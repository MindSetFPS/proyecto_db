from shopApp.models import User, Order, OrderDetail
from django.shortcuts import render, redirect

def profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        user_data = {
            'email': user.email,
            'username': user.username,
            'name': user.first_name,
            'last_name': user.last_name
        }
        
        last_order = Order.objects.filter(customer=user).order_by('-date').first()
        last_order_products = OrderDetail.objects.filter(order=last_order).all()
        amount_of_products = len(last_order_products)
        
        for product in last_order_products:
            product.image = product.product.image_set.first()
            
        for product in last_order_products:
            print(product.image)

        return render(
            request, 
            'profile.html', 
            {
                'profile': user_data, 
                'order': last_order, 
                'products': last_order_products[:4], 
                'amount_of_products': amount_of_products
            }
        )
    # r:eturn HttpResponse(request.session.session_key)
    return redirect('login')