from django.test import TestCase
from django.contrib.auth.models import User
from shopApp.models import Category, Product, Order, OrderDetail, ShoppingCart, Customer

## LISTA
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10,
            description="A high-end laptop",
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.description, "A high-end laptop")
        self.assertEqual(self.product.category, self.category)
