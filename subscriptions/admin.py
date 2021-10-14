from django.contrib import admin
from .models import Subscription, Order, Payment

admin.site.register(Subscription)
admin.site.register(Order)
admin.site.register(Payment)
