from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

def order_history(request: HttpRequest):
    return render(request, 'order-history.html')