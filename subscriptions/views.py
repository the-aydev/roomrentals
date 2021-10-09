from django.contrib import messages, auth
from .models import Subscription, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
import json


def simpleCheckout(request):
    return render(request, 'subscriptions/simple_checkout.html')


def subscription(request):
    subscriptions = Subscription.objects.all()
    context = {'subscriptions': subscriptions}
    return render(request, 'subscriptions/subscription.html', context)


def checkout(request, pk):
    subscription = Subscription.objects.get(id=pk)
    context = {'subscription': subscription}
    return render(request, 'subscriptions/checkout.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    return JsonResponse('Payment completed!', safe=False)
