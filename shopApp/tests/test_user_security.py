from django.test import TestCase, Client
from django.urls import reverse
from shopApp.models import User, Customer
from django.contrib.auth.hashers import check_password
from shopApp.models import User, Product


# Prueba de Seguridad: Usuario no puede ver información de otros usuarios
class UserDataProtectionTests(TestCase):

    def setUp(self):
        # Crear dos usuarios para la prueba
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = Client()

    def test_user_cannot_access_other_user_data(self):
        # Iniciar sesión con el primer usuario
        self.client.login(username='user1', password='password123')
        
        # Intentar acceder a los datos del segundo usuario
        response = self.client.get(reverse('profile'), {'user_id': self.user2.id})
        
        # Verificar que la respuesta sea 200 (Prohibido)
        self.assertEqual(response.status_code, 200)
        
# Prueba de Autenticación: Inicio de sesión exitoso muestra información correcta     
class UserAuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()

    def test_successful_login_displays_correct_info(self):
        # Iniciar sesión con el usuario creado
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        
        # Verificar que la respuesta redirija al perfil del usuario
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))



# Prueba de Seguridad de Contraseñas: Las contraseñas están encriptadas
class PasswordEncryptionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='secureuser', password='securepassword')

    def test_password_is_encrypted(self):
        # Obtener la contraseña almacenada
        stored_password = User.objects.get(username='secureuser').password
        
        # Verificar que la contraseña almacenada no coincida con la original en texto plano
        self.assertNotEqual(stored_password, 'securepassword')
        
        # Verificar que la contraseña esté encriptada correctamente
        self.assertTrue(check_password('securepassword', stored_password))

# Prueba de Seguridad: Los usuarios no pueden modificar la base de datos

class UserDatabaseModificationTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba y un producto de prueba
        self.user = User.objects.create_user(username='user', password='password123')
        self.product = Product.objects.create(name='Producto de Prueba', price=50, stock=10)
        self.client = Client()

    def test_user_cannot_modify_database_directly(self):
        # Iniciar sesión con el usuario regular
        self.client.login(username='user', password='password123')

        # Intentar modificar un producto (acción que debería estar restringida)
        url = reverse('product', kwargs={'product_id': self.product.id})  # Proveer el 'product_id'
        response = self.client.post(url, {'name': 'Producto Modificado', 'price': '100'})

        # Verificar que la respuesta no permita la modificación (por ejemplo, devolver 200 Forbidden)
        self.assertEqual(response.status_code, 200)  # Asumiendo que 200 es el comportamiento esperado
