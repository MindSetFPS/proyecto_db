from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from shopApp.models import Order, Customer, OrderDetail

@login_required
def order(request: HttpRequest, order_id):
    # Redirect if order does not exist
    
    order = Order.objects.get(pk = order_id)
    customer = Customer.objects.filter(user=order.customer).first()
    products = OrderDetail.objects.filter(order = order_id).all()
    
    for product in products:
        product.image = product.product.image_set.first()
    print(order)
    print(customer)
    print(products)
    return render(request, 'order.html', {'order': order, 'customer': customer, 'products': products})