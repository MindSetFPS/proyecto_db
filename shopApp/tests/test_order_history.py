# shopApp/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Order, OrderDetail, Product, Image
from django.utils import timezone

class OrderHistoryViewTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a test client
        self.client = Client()

        # Log the user in
        self.client.login(username='testuser', password='12345')

        # Create a test product with an image
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.image = Image.objects.create(product=self.product, url='http://example.com/image.jpg')

        # Create a test order
        self.order = Order.objects.create(customer=self.user, date=timezone.now())

        # Create test order details
        for i in range(5):
            OrderDetail.objects.create(order=self.order, product=self.product, quantity=1)

    def test_order_history_view(self):
        response = self.client.get(reverse('order_history'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'order-history.html')

        # Check that the orders are in the context
        self.assertIn('orders', response.context)

        # Check that the order has the correct number of products
        orders = response.context['orders']
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].amount_of_products, 5)

        # Check that limited items are correctly set
        self.assertEqual(len(orders[0].items_limited), 4)
        for item in orders[0].items_limited:
            self.assertEqual(item.image.image_url, 'http://example.com/image.jpg')

