from django_slack import slack_message
from django.dispatch import receiver
from shop.models import UserProfile
from django.db.models.signals import post_save
# Code Starts Below


@receiver(post_save, sender=UserProfile)
def new_user_registered(sender, instance, created, **kwargs):
      if created:
            context = {
                "user": instance
            }
            return slack_message("shop/slack-notifications/new_user_registered.html", context)
