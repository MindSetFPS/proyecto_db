from django.test import TestCase

# Create your tests here.

# shopApp/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Order, OrderDetail, Product, Image
from datetime import datetime

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
