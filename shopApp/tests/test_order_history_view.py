from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Order, Product, Image, Category
import json
from unittest.mock import patch
from shopApp.admin import ProductAdmin

class OrderHistoryViewTests(TestCase):
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
        self.image = Image.objects.create(product=self.product, url='http://example.com/image.jpg')
        self.order = Order.objects.create(customer=self.user, total=999.99, status=1)
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_order_history_view(self):
        response = self.client.get(reverse('order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order-history.html')
        self.assertIn('orders', response.context)
        orders = response.context['orders']
        print(orders[0].items)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].amount_of_products, 0)
        self.assertEqual(len(orders[0].items), 0)
