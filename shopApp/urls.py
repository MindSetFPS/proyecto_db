from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('admin/my-custom-page/', my_custom_viewer, name='my_custom_viewer'),
    path("product/<int:product_id>", product, name="product"),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', login_user, name='login'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('buy_cart', buy_cart, name='buy_cart'),
    path('logout', logout_view, name='logout'),
    path('remove_product_cart/<int:product_id>', remove_product_cart, name='remove_product_cart'),
    path('decrease_cart_product/<int:product_id>', decrease_cart_product, name='decrease_cart_product'),
    path('categories/<str:category>', category, name='category'),
    path('order-history/', order_history, name='order_history'),
    path('order/<int:order_id>/', order, name='order'),
    path('buy', buy.buy_cart, name='buy'),
    path('payment', payment, name='payment'),
    path('notification', notification, name='notification'),
    path('success', success, name='success')
    # path('category/', views.category, name='category'),
]
