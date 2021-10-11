from .models import Code
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
