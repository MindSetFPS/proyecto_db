from django.shortcuts import render, redirect
from shopApp.models import ShoppingCart, Product, Order, OrderDetail
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
import mercadopago
import os


MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN')
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def buy_cart(request: HttpRequest):
    # If user is not authenticated, but has products in his product cart:w
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to registration page

    session_id = request.session.session_key
    # cart_items = ShoppingCart.objects.filter(session_id=session_id)

    if request.user.is_authenticated:
        # find shopping cart with user id
        cart_items = ShoppingCart.objects.filter(user=request.user)

    if not cart_items.exists():
        return HttpResponse("No items in cart")

    total = 0
    # Purchase products

    items = []
    for item in cart_items:
        prod = Product.objects.get(id=item.product_id)
        if prod.stock >= item.amount:
            mp_product = {
                "id": prod.id,
                "title": prod.name,
                "currency_id": "MXN",
                "picture_url": "https://i.postimg.cc/Gp0X9MK2/baphomet-frente.jpg",
                "description": prod.description,
                "category_id": "art",
                "quantity": item.amount,
                "unit_price": float(prod.price) #This may throw an error
            }
            prod.stock -= item.amount
            prod.save()
            items.append(mp_product)
            total = total + prod.price
        else:
            return redirect('view_cart')
        item.delete()  # Remove the cart item after purchase

    order = Order(customer=request.user, total=total, status=0)
    order.save()

    # Cannot create order_detail, because order is not created yet
    for item in cart_items:
        prod = Product.objects.get(id=item.product_id)
        # TODO: OrderDetatil should be able to be created without order
        order_detail = OrderDetail(order=order, product=prod, quantity=item.amount)
        order_detail.save()

    preference_data = {
        "items": items,
        "payer": {
            "name": request.user.first_name,
            "surname": request.user.last_name,
            "email": request.user.email,
            "phone": {
                "area_code": "11",
                "number": "4444-4444"
            },
            "identification": {
                "type": "CPF",
                "number": "19119119100"
            },
            "address": {
                "street_name": "Street",
                "street_number": 123,
                "zip_code": "06233200"
            }
        },
        "back_urls": {
            "success": settings.SITE_URL + '/success',
            "failure": settings.SITE_URL + '/failure',
            "pending": settings.SITE_URL + '/pending'
        },
        "auto_return": "approved",
        # This needs an URL with https
        "notification_url": settings.SITE_URL + "/notification",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        "expires": True,
        # "expiration_date_from": "2016-02-01T12:00:00.000-04:00",
        # "expiration_date_to": "2016-02-28T12:00:00.000-04:00"
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    print(preference)
    return JsonResponse(preference)
    # return render(request, 'purchase_successful.html', {'total_price': total})

def success(request: HttpRequest):
    return render(request,'success.html')