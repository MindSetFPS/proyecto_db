from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
import mercadopago
import os, json, hmac, hashlib
# from django.conf.global_settings import 

MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN')
# MP_PRIVATE_KEY = os.environ['MP_PRIVATE_KEY']

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

def buy(request):
    return render(request, 'buy.html')

def payment(request):
    # Generate payment link based on product
    preference_data = {
        "items": [
            {
                "id": "item-ID-1234",
                "title": "Gatito Tejedor",
                "currency_id": "MXN",
                "picture_url": "https://i.postimg.cc/Gp0X9MK2/baphomet-frente.jpg",
                "description": "Descrição do Item",
                "category_id": "art",
                "quantity": 1,
                "unit_price": 75.76
            }
        ],
        "payer": {
            "name": "João",
            "surname": "Silva",
            "email": "user@email.com",
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
            "success": "https://www.success.com",
            "failure": "http://www.failure.com",
            "pending": "http://www.pending.com"
        },
        "auto_return": "approved",
        # This needs an URL with https
        "notification_url": "https://ced8-2806-10b7-3-92f4-00-1.ngrok-free.app/notification",
        "statement_descriptor": "MEUNEGOCIO",
        "external_reference": "Reference_1234",
        "expires": True,
        # "expiration_date_from": "2016-02-01T12:00:00.000-04:00",
        # "expiration_date_to": "2016-02-28T12:00:00.000-04:00"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return JsonResponse(preference)
    
# This needs an URL with https
@csrf_exempt
def notification(request):
    data_id = request.GET.get('id') or request.GET.get('data.id')
    notification_type = request.GET.get('type')
    
    x_signature = request.META['HTTP_X_SIGNATURE']
    x_request_id = request.META['HTTP_X_REQUEST_ID']

    x_signature = x_signature.split(",")
    x_signature_ts = x_signature[0]
    ts = x_signature_ts.split("=")[1]
    x_signature_v1 = x_signature[1]
    hashed_v1 = x_signature_v1.split("=")[1]
    
    manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
    secret = os.environ.get('MP_WEBHOOK_SECRETE_KEY')
    
    hmac_obj = hmac.new(secret.encode(), msg=manifest.encode(), digestmod=hashlib.sha256)
    sha = hmac_obj.hexdigest()

    if sha == hashed_v1:
        # HMAC verification passed
        # Confirm payment
        print("HMAC verification passed")
        
        return HttpResponse('')
    else:
        # HMAC verification failed
        # Reject request
        print("HMAC verification failed")
        return HttpResponseBadRequest(content="Invalid signature")
