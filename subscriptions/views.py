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

# def verify(request, ref):
#     payment = get_object_or_404(Payment, ref=ref)
#     verified = payment.verify_payment()
#     if verified:
#         messages.success(request, "Verification successful!")
#     else:
#         messages.error(request, "Verification failed!")
#     return redirect('/subscriptions/subscription')

def verify(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data


# def verify(request, id)
#     plan = Plan(authorization_key=settings.PAYSTACK_SECRET_KEY)
#     response = plan.create("Silver", 100, 'Monthly')
#     response = plan.create("Gold", 200, 'Monthly')
#     response = plan.create("Platinum", 300, 'Monthly')
#     response = plan.getall()
#     response = plan.verify(id)
#     data = JsonResponse(response, safe=False)
#     return data
