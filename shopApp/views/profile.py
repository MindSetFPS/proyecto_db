from shopApp.models import User, Order, OrderDetail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def profile(request):
    if request.user.is_authenticated:
        print(settings.SITE_URL)
        user = User.objects.get(pk=request.user.id)
        user_data = {
            'email': user.email,
            'username': user.username,
            'name': user.first_name,
            'last_name': user.last_name
        }
        
        last_order = Order.objects.filter(customer=user).order_by('-date').first()
        last_order_products = OrderDetail.objects.filter(order=last_order).all()
        last_order_products.amount_of_products = len(last_order_products)
        if last_order is not None:
            last_order.amount_of_products = len(last_order_products)
        
        for product in last_order_products:
            product.image = product.product.image_set.first()
            
        return render(
            request, 
            'profile.html', 
            {
                'profile': user_data, 
                'order': last_order, 
                'products': last_order_products[:4], 
            }
        )
    return redirect('login')