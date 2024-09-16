from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Customer, Order, Category, Image

## 5 ADMIN SITE TESTS ##
class AdminSiteTests(TestCase):
    def setUp(self):
        # Create a superuser for accessing the admin site
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.client.force_login(self.admin_user)
        
        # Create some test data
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=10.0,
            stock=100,
            description='Test Description'
        )
        self.customer = Customer.objects.create(user=self.admin_user, address='Test Address')
        self.order = Order.objects.create(customer=self.customer, total=100.0)
        self.image = Image.objects.create(product=self.product, url='http://example.com/image.jpg')

    def test_product_admin_registered(self):
        self.assertTrue(site.is_registered(Product))

    def test_order_admin_registered(self):
        self.assertTrue(site.is_registered(Order))

    def test_category_admin_registered(self):
        self.assertTrue(site.is_registered(Category))

    def test_image_admin_registered(self):
        self.assertTrue(site.is_registered(Image))

    def test_user_admin_registered(self):
        self.assertTrue(site.is_registered(get_user_model()))

    def test_product_list_display(self):
        product_admin = site._registry[Product]
        self.assertEqual(product_admin.list_display, ('Imagen', 'name', 'price', 'stock', 'category'))

    def test_order_list_display(self):
        order_admin = site._registry[Order]
        self.assertEqual(order_admin.list_display, ('id', 'date', 'customer_id', 'total'))

    def test_category_list_display(self):
        category_admin = site._registry[Category]
        self.assertEqual(category_admin.list_display, ('name',))

    def test_product_detail_view(self):
        url = reverse('admin:shopApp_product_change', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_order_detail_view(self):
        url = reverse('admin:shopApp_order_change', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order')

    def test_category_detail_view(self):
        url = reverse('admin:shopApp_category_change', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_image_detail_view(self):
        url = reverse('admin:shopApp_image_change', args=[self.image.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http://example.com/image.jpg')

    def test_user_detail_view(self):
        url = reverse('admin:auth_user_change', args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin@example.com')
