from django.contrib import admin
# Register your models here.
from .models import Product, Customer, Order, OrderDetail, Category, Image
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ['date', 'total']
    readonly_fields = ['date', 'total']
    show_change_link = True

class UserProfileInline(admin.TabularInline):
    model = Customer
    verbose_name = "Customer Details"

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline, OrderInline]

class ProductInline(admin.TabularInline):
    model = OrderDetail
    extra = 0

    def product_name(self, instance):
        return instance.product.name

    readonly_fields = ['product_name']
    fields = ('product_name', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    readonly_fields = ['customer', 'total']
    list_display = ('id', 'date', 'customer_id', 'total')

class CategoryAdmin(admin.ModelAdmin):
    fields = [('name', 'parent')]
    list_display = ('name',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ('url',)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    fields = ('name', 'category', 'price', 'stock', 'description')
    list_display = ( "Imagen", 'name', 'price', 'stock', 'category')
    list_editable = ('price', 'stock')
    list_display_links = ('name', )
    
    def Imagen(self, obj):
        return format_html('<img src="%s" class="img-fluid" style="object-fit: contain;" />' % Image.objects.filter(product=obj).first().url)
    Imagen.allow_tags = True

admin.site.site_header = "Gatito tejedor"

admin.site.unregister(User) # Should unregister User to modify it as is preregistered 
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)