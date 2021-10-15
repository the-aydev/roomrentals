from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Message(models.Model):

    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)
