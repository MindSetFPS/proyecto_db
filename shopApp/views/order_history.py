from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from shopApp.models import Order, User, OrderDetail
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request: HttpRequest):

    user = User.objects.get(pk=request.user.id)
    orders = Order.objects.filter(customer=user).order_by('-date').all()

    for order in orders:
        order.items = OrderDetail.objects.filter(order=order).all()
        order.amount_of_products = len(order.items)
        order.items = order.items[:4]

        for item in order.items:
            item.image = item.product.image_set.first()

    return render(request, 'order-history.html', {'orders':orders})