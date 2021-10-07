from django.db import models
from datetime import datetime
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=100)


class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=100)
