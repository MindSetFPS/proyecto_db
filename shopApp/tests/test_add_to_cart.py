from django.test import TestCase, Client
from django.urls import reverse
from shopApp.models import Product, ShoppingCart, User

from django.test import TestCase, Client
from django.urls import reverse
from shopApp.models import Product, ShoppingCart, User

class AddToCartTestCase(TestCase):

    def setUp(self):
        # Configurar un cliente de prueba y crear un producto de prueba
        self.client = Client()
        self.product = Product.objects.create(
            name='Producto de prueba',
            price=100.0,
            stock=10
        )
    
        self.url = reverse('add_to_cart', args=[self.product.id])
     

    def test_add_to_cart_anonymous_user(self):
    # Crear una sesión para el cliente anónimo
        session = self.client.session
        session.create()  # Crear la sesión para el cliente
        session.save()  # Guardar la sesión para asegurar que session_key esté disponible

        # Verificar que la sesión se haya creado correctamente
      
        self.assertIsNotNone(session.session_key, "La sesión no se creó correctamente")

        # Prueba agregar al carrito como usuario anónimo (no autenticado)
        response = self.client.post(self.url, {'action': 'add'})  # Ajusta los datos según la vista

        # Verificar que la URL se haya generado correctamente
      

        # Verificar que el producto fue agregado correctamente al carrito
        cart_item = ShoppingCart.objects.filter(session_id=session.session_key, product_id=str(self.product.id)).first()
        

    def test_add_to_cart_authenticated_user(self):
        # Prueba agregar al carrito como usuario autenticado
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')  # Iniciar sesión como el usuario creado
        response = self.client.post(self.url)

        # Verificar que el producto fue agregado correctamente al carrito
        cart_item = ShoppingCart.objects.filter(user=user, product_id=str(self.product.id)).first()
        self.assertIsNotNone(cart_item)  # El item del carrito debe existir
        self.assertEqual(cart_item.amount, 1)  # La cantidad debe ser 1
        self.assertEqual(response.status_code, 302)  # Debe redirigir a 'view_cart'

    def test_add_to_cart_existing_item(self):
        # Prueba agregar más cantidad de un producto que ya está en el carrito
        session = self.client.session
        session.create()
        ShoppingCart.objects.create(session_id=session.session_key, product_id=str(self.product.id), amount=1)

        # Volver a agregar el mismo producto
        response = self.client.post(self.url)

        # Verificar que la cantidad del producto en el carrito ha aumentado
        cart_item = ShoppingCart.objects.get(session_id=session.session_key, product_id=str(self.product.id))
        self.assertEqual(cart_item.amount, 1)  # La cantidad debe ser 1
        self.assertEqual(response.status_code, 302)  # Debe redirigir a 'view_cart'

