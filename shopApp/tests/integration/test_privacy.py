from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserPrivacyTest(TestCase):

    def setUp(self):
        # Crear dos usuarios para la prueba
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')

    def test_user_cannot_access_other_user_data(self):
        """Verifica que un usuario no pueda ver los datos de otro usuario"""
        # Iniciar sesión como user1
        self.client.login(username='user1', password='pass1234')
        # Intentar acceder a los datos de user2
        response = self.client.get(reverse('user_data', kwargs={'user_id': self.user2.id}))
        # Debe devolver un código 403 (acceso prohibido)
        self.assertEqual(response.status_code, 403)

    def test_unregistered_cannot_access_user_data(self):
        """Verifica que los usuarios no registrados no puedan acceder a datos de usuarios"""
        # Intentar acceder a los datos de user1 sin iniciar sesión
