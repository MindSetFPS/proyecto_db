from django.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Category, Order, Customer, OrderDetail, Product, Image, ShoppingCart
from django.utils import timezone
from datetime import datetime
from unittest.mock import patch
import json
from shopApp.forms import UserRegistrationForm, LoginForm
from shopApp.context_processor import my_context_processor, categories, profile_links
## 1
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.product_image = Image.objects.create(product=self.product, url='path/to/image.jpg')
        self.order = Order.objects.create(customer=self.user, date=datetime.now())
        self.order_detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=1)

    def test_profile_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIn('profile', response.context)
        self.assertIn('order', response.context)
        self.assertIn('products', response.context)
        self.assertEqual(response.context['profile']['email'], 'testuser@example.com')
        self.assertEqual(response.context['order'], self.order)
        self.assertEqual(len(response.context['products']), 1)
        # self.assertEqual(response.context['products'][0].image, 'path/to/image.jpg')

    # def test_profile_view_unauthenticated_user(self):
    #     response = self.client.get(reverse('profile'))
    #     self.assertRedirects(response, reverse('login'))
## 2
class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, address='123 Test St')
        self.product = Product.objects.create(name='Test Product', price=10.00, stock=10, description='Test Description')
        self.image = Image.objects.create(product=self.product, url='http://example.com/image.jpg')
        self.order = Order.objects.create(customer=self.user, total=10.00)
        self.order_detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=1)

    def test_order_view_redirects_if_not_logged_in(self): ## Este funciona pero al estar el siguiente test manda error.
        response = self.client.get(reverse('order', args=[self.order.id]))
        login_url = f"{reverse('login')}?next={reverse('order', args=[self.order.id])}"
        self.assertRedirects(response, login_url, status_code=302, target_status_code=200)

    def test_order_view_displays_correctly_for_logged_in_user(self): ## Error
       self.client.login(username='testuser', password='testpassword')
       response = self.client.get(reverse('order', args=[self.order.id]))
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'order.html')
       self.assertContains(response, self.order.total)
       self.assertContains(response, self.customer.address)
       self.assertContains(response, self.product.name)
       self.assertContains(response, self.image.url)

    def test_order_view_redirects_if_order_does_not_exist(self):  ## Error
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order', args=[999]))
        self.assertEqual(response.status_code, 404)


## 3
class OrderHistoryViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a product and images
        self.product = Product.objects.create(name='Test Product', price=10.00)
        self.image = Image.objects.create(product=self.product, image='test_image.jpg')

        # Create an order
        self.order = Order.objects.create(customer=self.user, date=timezone.now())

        # Create order details
        self.order_detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=2)

        # Create a client and log in
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_order_history_view(self):
        response = self.client.get(reverse('order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order-history.html')
        self.assertIn('orders', response.context)
        orders = response.context['orders']
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].amount_of_products, 1)
        self.assertEqual(len(orders[0].items), 1)
        self.assertEqual(orders[0].items[0].image, self.image)

## 4
# shopApp/tests/test_payment.py
## asecurarse que este intelado django and reqquest-mock para este test
class PaymentViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('mercadopago.SDK.preference')
    def test_payment_view(self, mock_preference):
        # Mock the response from mercadopago
        mock_preference().create.return_value = {
            "response": {
                "id": "123456789",
                "init_point": "https://www.mercadopago.com/init_point",
                "sandbox_init_point": "https://www.mercadopago.com/sandbox_init_point"
            }
        }

        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('id', json.loads(response.content))
        self.assertIn('init_point', json.loads(response.content))

    @patch('shopApp.views.payment.hmac.new')
    @patch('shopApp.views.payment.os.environ.get')
    def test_notification_view(self, mock_os_environ_get, mock_hmac_new):
        # Mock environment variable and HMAC object
        mock_os_environ_get.return_value = 'dummy_secret'
        mock_hmac_obj = mock_hmac_new.return_value
        mock_hmac_obj.hexdigest.return_value = 'valid_hmac_signature'

        headers = {
            'HTTP_X_SIGNATURE': 'ts=1234567890,v1=valid_hmac_signature',
            'HTTP_X_REQUEST_ID': 'request_id_123'
        }
        response = self.client.post(reverse('notification'), data={'id': 'data_id_123'}, **headers)
        self.assertEqual(response.status_code, 200)

        # Test invalid HMAC signature
        mock_hmac_obj.hexdigest.return_value = 'invalid_hmac_signature'
        response = self.client.post(reverse('notification'), data={'id': 'data_id_123'}, **headers)
        self.assertEqual(response.status_code, 400)

## 6 models
# shopApp/tests/test_models.py

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10,
            description="A high-end laptop",
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.description, "A high-end laptop")
        self.assertEqual(self.product.category, self.category)

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(customer=self.user, total=199.99)

    def test_order_creation(self):
        self.assertEqual(self.order.customer.username, 'testuser')
        self.assertEqual(self.order.total, 199.99)

class OrderDetailModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10,
            description="A high-end laptop",
            category=self.category
        )
        self.order = Order.objects.create(customer=self.user, total=999.99)
        self.order_detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=1)

    def test_order_detail_creation(self):
        self.assertEqual(self.order_detail.order, self.order)
        self.assertEqual(self.order_detail.product, self.product)
        self.assertEqual(self.order_detail.quantity, 1)

class ShoppingCartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.shopping_cart = ShoppingCart.objects.create(
            session_id="session123",
            user=self.user,
            product_id="prod123",
            amount=2
        )

    def test_shopping_cart_creation(self):
        self.assertEqual(self.shopping_cart.session_id, "session123")
        self.assertEqual(self.shopping_cart.user.username, 'testuser')
        self.assertEqual(self.shopping_cart.product_id, "prod123")
        self.assertEqual(self.shopping_cart.amount, 2)

class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, address="123 Main St")

    def test_customer_creation(self):
        self.assertEqual(self.customer.user.username, 'testuser')
        self.assertEqual(self.customer.address, "123 Main St")

## 7 urls


class IndexViewTests(TestCase):

    def test_index_view_status_code(self):
        """
        Test that the index view returns a 200 status code.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """
        Test that the index view uses the correct template.
        """
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_content(self):
        """
        Test that the index view renders the correct content.
        """
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Welcome to the ShopApp")  # Adjust this to match your actual content


## 8 forms


class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password2': 'password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password2': 'password321',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['Password mismatch'])

class LoginFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'password123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_username(self):
        form_data = {
            'password': 'password123',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_form_missing_password(self):
        form_data = {
            'username': 'testuser',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

## 9 context_processors.py
# shopApp/tests/test_context_processors.py



class ContextProcessorTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_my_context_processor(self):
        context = my_context_processor(self.request)
        self.assertIn('custom', context)
        self.assertEqual(context['custom'], 'Hello from processor')

    def test_categories(self):
        # Create some test categories
        Category.objects.create(name='Category 1')
        Category.objects.create(name='Category 2', parent=None)
        Category.objects.create(name='Category 3', parent=None)

        context = categories(self.request)
        self.assertIn('categories', context)
        self.assertEqual(len(context['categories']), 3)
        self.assertQuerysetEqual(
            context['categories'],
            ['<Category: Category 1>', '<Category: Category 2>', '<Category: Category 3>'],
            ordered=False
        )

    def test_profile_links(self):
        context = profile_links(self.request)
        self.assertIn('links', context)
        self.assertEqual(len(context['links']), 4)
        self.assertEqual(context['links'][0]['url'], 'profile')
        self.assertEqual(context['links'][1]['url'], 'logout')
        self.assertEqual(context['links'][2]['url'], 'register')
        self.assertEqual(context['links'][3]['url'], 'login')

## 10