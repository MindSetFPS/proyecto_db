# shopApp/tests/test_views.py
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Order, Product, Category, Image

class OrderViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a category
        self.category = Category.objects.create(name='Test Category')
        
        # Create an order
        self.order = Order.objects.create(
            customer=self.user,
            total=100.50,
            status=1
        )
        # Create a product and associate it with the order
        self.product = Product.objects.create(name='Test Product', price='2000',stock='20',description='Test Description', category=self.category)
        # Create an image and associate it with the product
        self.image = Image.objects.create(product=self.product, url='http://example.com/image.jpg') 
        # URL for the order view
        self.url = reverse('order', args=[self.order.id])
        
    def test_order_view_with_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')   
        # Make a GET request to the order view
        response = self.client.get(self.url) 
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template is used
        self.assertTemplateUsed(response, 'order.html')
        # Check that the order and products are in the context
        self.assertIn('order', response.context)
        self.assertIn('products', response.context)

    def test_order_view_with_unauthenticated_user(self):
        # Make a GET request to the order view without logging in
        response = self.client.get('/login')
        
     
