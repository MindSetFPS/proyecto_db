from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Order, Product, Image, Category
import json
from unittest.mock import patch
from shopApp.admin import ProductAdmin

## LISTO
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
        self.image = Image.objects.create(product=self.product, image_url='http://example.com/image.jpg') ## se cambio en la bd de image.url a image_url
        self.order = Order.objects.create(customer=self.user, total=999.99,status='2')
        self.order.items.add(self.product, through_defaults={'quantity': 1})

        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_order_history_view(self):
        response = self.client.get(reverse('order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order-history.html')
        self.assertIn('orders', response.context)
        orders = response.context['orders']
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].items.count(), 1)
        first_image = orders[0].items.first().image_set.first()    
        self.assertEqual(first_image, self.image)
