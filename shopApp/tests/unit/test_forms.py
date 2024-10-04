from django.test import TestCase
from django.contrib.auth.models import User
from shopApp.forms import UserRegistrationForm, LoginForm

## LISTA ##
class UserRegistrationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password2': 'differentpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['Password mismatch'])

    def test_missing_fields(self):
        form_data = {
            'username': 'userexample',
            'email': 'example@example.com',
            'password': '12342',
            'password2': '12342'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        

class LoginFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_fields(self):
        form_data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)
