from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tub


@receiver(post_save, sender=Tub)
def notify_if_empty(sender, instance, **kwargs):
    if instance.scoops_left == 0:
        instance.notify_admin_of_low_scoops()
