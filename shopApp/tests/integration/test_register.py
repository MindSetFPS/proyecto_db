from django.urls import reverse
from django.test import TestCase, Client
from shopApp.models import User, ShoppingCart, Customer
from django.contrib.auth.hashers import check_password

class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }

    def test_register_user_successfully(self):
        response = self.client.post(reverse('register'), data=self.user_data)
        self.assertEqual(response.status_code, 302)

        # Check if the user is created
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])

        # Check if cart items are migrated to new user
        shopping_cart_item = ShoppingCart.objects.create(session_id='test_session', product_id='product123', amount=1)
        shopping_cart_item.user = user
        shopping_cart_item.save()
        self.assertEqual(shopping_cart_item.user, user)

        # Check if customer object is created
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.address, '')

    def test_register_user_with_invalid_data(self):
        invalid_data = {
            'username': '',
            'email': 'invalid_email',
            'password': 'short_password',
            'password2': 'short_password23'
        }
        response = self.client.post(reverse('register'), data=invalid_data)
        self.assertEqual(response.status_code, 200)