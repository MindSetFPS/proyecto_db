from django.test import TestCase, Client
from django.urls import reverse
from shopApp.models import User

class UserCreationSpacesTestCase(TestCase):

    def setUp(self):
        # Crear un usuario base con un `username` y `email` sin espacios
        self.base_user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.client = Client()

    def test_create_user_with_leading_and_trailing_spaces_in_username(self):
        # Intentar crear un nuevo usuario con espacios al principio y al final del `username`
        response = self.client.post(reverse('register'), {
            'username': '  testuser  ',  # Espacios al inicio y al final
            'password': 'password123',
            'password2': 'password123',
            'email': 'unique_email@example.com'
        })
        # Verificar que no se pueda crear un usuario con el mismo nombre pero con espacios
        self.assertEqual(response.status_code, 200)  # El código debe ser 200 porque la creación no debe ser exitosa
        self.assertContains(response, "El nombre de usuario ya existe")  # Mensaje de error esperado

    def test_create_user_with_intermediate_spaces_in_username(self):
        # Intentar crear un usuario con espacios intermedios en el `username`
        response = self.client.post(reverse('register'), {
            'username': 'test user',  # Espacio intermedio
            'password': 'password123',
            'password2': 'password123',
            'email': 'unique_email@example.com'
        })
        # Validar que se rechace el registro de este `username`
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se permiten espacios en el nombre de usuario")

    def test_create_user_with_leading_and_trailing_spaces_in_email(self):
        # Intentar crear un nuevo usuario con espacios al principio y al final del `email`
        response = self.client.post(reverse('register'), {
            'username': 'unique_username',
            'password': 'password123',
            'password2': 'password123',
            'email': '  test@example.com  '  # Espacios al inicio y al final
        })
        # Verificar que no se pueda crear un usuario con el mismo `email` pero con espacios
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El correo electrónico ya está en uso")

    def test_create_user_with_intermediate_spaces_in_email(self):
        # Intentar crear un nuevo usuario con un `email` con espacios intermedios
        response = self.client.post(reverse('register'), {
            'username': 'unique_username',
            'password': 'password123',
            'password2': 'password123',
            'email': 'test @example.com'  # Espacio intermedio
        })
        # Validar que se rechace el registro de este `email`
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Correo electrónico no válido")
