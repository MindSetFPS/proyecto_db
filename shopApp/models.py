from django.db import models 
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class ShoppingCart(models.Model):
    session_id = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    product_id = models.CharField(max_length=255, null=False)  # Assuming product_id is a string
    amount = models.IntegerField(default=0)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    address = models.CharField(max_length=255)

# Pedido
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)

class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', null=True, blank=True ,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=16,decimal_places=2)
    stock = models.IntegerField(db_default=0)
    description = RichTextField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

#PedidoDetalle
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=0)
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField(max_length=1023)
    
# TODO: Auditorías
# class Auditoria(models.Model):
#     pass