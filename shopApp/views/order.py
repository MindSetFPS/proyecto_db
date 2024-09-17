# Example view (shopApp/views/order.py)
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from shopApp.models import Order

@login_required
def order(request, order_id):
    # Get the order object or return a 404 error if it doesn't exist
    order = get_object_or_404(Order.objects.select_related('category'), id=order_id)
    products = order.products.all()  # Assuming Order has a related name 'products'
    #customer = Customer.objects.filter(user=order.customer).first()

    # Assuming each product has an image set and we need the first image
    for product in products:
        product.image = product.image_set.first()
    return render(request, 'order.html', {'order': order, 'products': products})
