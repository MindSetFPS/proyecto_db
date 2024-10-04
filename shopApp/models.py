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
# TODO: customer FK should be Customer model, not User model(analyze ramifications of this mistake)
class Order(models.Model):
    items = models.ManyToManyField('Product', through='OrderDetail')
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Elimina el default si no es necesario
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Status(models.IntegerChoices):
        PROCESSING = 1, "Processing"
        READY = 2, "Ready to ship"
        ON_THE_WAY = 3, "On the way"
        DELIVERED = 4, "Delivered"

    status = models.IntegerField(choices=Status.choices, default=Status.PROCESSING)

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"

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
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'
    
class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1023)
    
    def __str__(self):
        return self.image_url
# TODO: Auditorías
# class Auditoria(models.Model):
#     pass