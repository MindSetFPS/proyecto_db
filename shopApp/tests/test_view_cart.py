from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopApp.models import Product, ShoppingCart, Image

class ViewCartTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Crear productos de prueba
        self.product1 = Product.objects.create(name='Producto 1', price=10.0, stock=5)
        self.product2 = Product.objects.create(name='Producto 2', price=20.0, stock=3)

        # Crear carrito de compras para el usuario autenticado
        self.cart_item_user1 = ShoppingCart.objects.create(user=self.user, product_id=str(self.product1.id), amount=2)
        self.cart_item_user2 = ShoppingCart.objects.create(user=self.user, product_id=str(self.product2.id), amount=1)

        # Crear carrito de compras para usuario anónimo (identificado por sesión)
        self.anonymous_session_id = 'test_session_id'
        self.cart_item_anon = ShoppingCart.objects.create(session_id=self.anonymous_session_id, product_id=str(self.product1.id), amount=1)

        # Crear imagen para los productos
        Image.objects.create(product=self.product1, image_url="https://example.com/product1.jpg")
        Image.objects.create(product=self.product2, image_url="https://example.com/product2.jpg")

        # Configurar cliente de prueba
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_view_cart_authenticated_user(self):
        # Probar la vista con un usuario autenticado
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingcar.html')
        
        # Verificar que se están mostrando los productos en el carrito del usuario autenticado
        self.assertIn('products', response.context)
        products = response.context['products']
        self.assertEqual(len(products), 2)  # El usuario tiene 2 productos en su carrito

        # Verificar que los totales sean correctos
        self.assertEqual(response.context['total_price'], 40.0)  # 2 * 10.0 + 1 * 20.0 = 40.0
        self.assertEqual(response.context['item_count'], 3)  # 2 + 1 = 3

    def test_view_cart_anonymous_user(self):
        # Probar la vista con un usuario anónimo
        session = self.client.session
        session['session_key'] = self.anonymous_session_id
        session.save()

        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingcar.html')

        # Verificar que se están mostrando los productos en el carrito del usuario anónimo
        self.assertIn('products', response.context)
        products = response.context['products']
        self.assertEqual(len(products), 2)  # El usuario anónimo tiene 1 producto en su carrito

        # Verificar que los totales sean correctos
        self.assertEqual(response.context['total_price'], 40.00)  # 1 * 10.0 = 10.0
        self.assertEqual(response.context['item_count'], 3)  # Solo un producto en el carrito

    def test_view_cart_empty_cart(self):
        # Probar la vista con un carrito vacío para un usuario autenticado
        ShoppingCart.objects.filter(user=self.user).delete()  # Eliminar los artículos del carrito
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingcar.html')
        self.assertEqual(len(response.context['products']), 0)  # No hay productos en el carrito
        self.assertEqual(response.context['total_price'], 0.0)  # Total debe ser 0
        self.assertEqual(response.context['item_count'], 0)  # No hay ítems en el carrito

    def test_view_cart_missing_session(self):
        # Probar la vista sin una sesión activa
        self.client.logout()
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shoppingcar.html')
        
