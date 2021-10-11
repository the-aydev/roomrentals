from django.contrib import admin
from .models import Subscription, Order, Payment

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Order)
admin.site.register(Payment)
