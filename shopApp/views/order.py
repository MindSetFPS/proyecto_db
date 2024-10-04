# Example view (shopApp/views/order.py)
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from shopApp.models import Order, Customer, OrderDetail

@login_required
def order(request, order_id):
    # Get the order object or return a 404 error if it doesn't exist
    order = Order.objects.get(pk = order_id)
    customer = Customer.objects.filter(user=order.customer).first()
    products = OrderDetail.objects.filter(order = order_id).all()

    # Assuming each product has an image set and we need the first image
    for product in products:
        product.image = product.image_set.first()
    return render(request, 'order.html', {'order': order, 'customer': customer, 'products': products})