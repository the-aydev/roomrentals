from django.conf import settings
from django.contrib import messages
from .models import Subscription, Order
from django.shortcuts import render
from django.http.response import JsonResponse
from pypaystack import Transaction, Customer, Plan
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# Paypal Integration

def subscription(request):
    subscriptions = Subscription.objects.all()
    users = User.objects.all()
    context = {
        'subscriptions': subscriptions,
        'pk_public': settings.PAYSTACK_PUBLIC_KEY,
        'users': users,
    }
    return render(request, 'subscriptions/subscription.html', context)


def checkout(request, pk):
    subscription = Subscription.objects.get(id=pk)
    context = {'subscription': subscription}
    return render(request, 'subscriptions/checkout.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    subscription = Subscription.objects.get(id=body['productId'])
    Order.objects.create(
        subscription=subscription
    )

    return JsonResponse('Payment completed!', safe=False)


# Paystack Integration

def verify(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data
