from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from shopApp.models import Order, User, OrderDetail
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request: HttpRequest):

    user = User.objects.get(pk=request.user.id)
    orders = Order.objects.filter(customer=user).order_by('-date').all()

    for order in orders:
        order_details = OrderDetail.objects.filter(order=order).all()
        order.amount_of_products = order_details.count()  # Número total de productos en la orden
        limited_items = order_details[:4]  # Limitar a los primeros 4 productos

        for item in limited_items:
            item.image = item.product.image_set.first()

        order.items_limited = limited_items  # Guardar los productos limitados para mostrarlos en la plantilla

    return render(request, 'order-history.html', {'orders': orders})
