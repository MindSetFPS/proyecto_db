from django.test import TestCase
from django.urls import reverse

class RegistrationTest(TestCase):
    def test_user_cannot_register_twice(self):
        # Registro inicial de usuario
        self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com'
        })
        
        # Intento de registro con el mismo usuario
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')
