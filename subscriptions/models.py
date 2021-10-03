from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    subscription = models.ForeignKey(
        Subscription, max_length=100, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscription.name
