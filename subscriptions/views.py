from django.conf import settings
from django.contrib import messages
from .models import Subscription, Order, Payment
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# Paypal Integration


def subscription(request):
    subscriptions = Subscription.objects.all()
    users = User.objects.all()
    context = {
        'subscriptions': subscriptions,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
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

def verify(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification successful!")
    else:
        messages.error(request, "Verification failed!")
    return redirect('/subscriptions/subscription')
