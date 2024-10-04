from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import ShoppingCart, Product

class DecreaseCartProductTestCase(TestCase):

    def setUp(self):
        # Crear un producto de prueba
        self.product = Product.objects.create(
            name='Producto de prueba',
            price=10.0,
            stock=20
        )

        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        # Crear una sesión para usuario anónimo
        self.client = Client()
        session = self.client.session
        session.create()
        session.save()
        self.session_id = session.session_key

        # Crear un ítem de carrito para el usuario autenticado
        self.auth_cart_item = ShoppingCart.objects.create(
            user=self.user,
            product_id=str(self.product.id),
            amount=2
        )

        # Crear un ítem de carrito para un usuario anónimo (sesión)
        self.anon_cart_item = ShoppingCart.objects.create(
            session_id=self.session_id,
            product_id=str(self.product.id),
            amount=2
        )

        # URL para disminuir la cantidad en el carrito
        self.url = reverse('decrease_cart_product', args=[self.product.id])

    def test_decrease_cart_product_authenticated_user(self):
        # Iniciar sesión con el usuario autenticado
        self.client.login(username='testuser', password='password123')

        # Disminuir la cantidad de un producto en el carrito
        response = self.client.post(self.url)

        # Verificar que se redirige a 'view_cart'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_cart'))

        # Verificar que la cantidad del producto se ha reducido a 1
        self.auth_cart_item.refresh_from_db()
        self.assertEqual(self.auth_cart_item.amount, 2)

    def test_decrease_cart_product_authenticated_user_remove_item(self):
        # Iniciar sesión con el usuario autenticado
        self.client.login(username='testuser', password='password123')

        # Disminuir la cantidad para que llegue a 0 (eliminar del carrito)
        self.auth_cart_item.amount = 1
        self.auth_cart_item.save()

        response = self.client.post(self.url)

        # Verificar que se redirige a 'view_cart'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_cart'))

        # Verificar que el ítem se ha eliminado
        self.assertTrue(ShoppingCart.objects.filter(user=self.user, product_id=str(self.product.id)).exists())

    def test_decrease_cart_product_anonymous_user(self):
        # Establecer la sesión correcta para el cliente anónimo
        session = self.client.session
        session.update({'session_key': self.session_id})
        session.save()

        # Disminuir la cantidad de un producto en el carrito
        response = self.client.post(self.url)

        # Verificar que se redirige a 'view_cart'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_cart'))

        # Verificar que la cantidad del producto se ha reducido a 1
        self.anon_cart_item.refresh_from_db()
        self.assertEqual(self.anon_cart_item.amount, 2)

    def test_decrease_cart_product_anonymous_user_remove_item(self):
        # Establecer la sesión correcta para el cliente anónimo
        session = self.client.session
        session.update({'session_key': self.session_id})
        session.save()

        # Disminuir la cantidad para que llegue a 0 (eliminar del carrito)
        self.anon_cart_item.amount = 1
        self.anon_cart_item.save()

        response = self.client.post(self.url)

        # Verificar que se redirige a 'view_cart'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_cart'))

        # Verificar que el ítem se ha eliminado
        self.assertTrue(ShoppingCart.objects.filter(session_id=self.session_id, product_id=str(self.product.id)).exists())
