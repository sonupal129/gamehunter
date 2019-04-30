from post_office import mail
from django.dispatch import receiver
from shop.models import UserProfile
from django.db.models.signals import pre_save, post_save
# Code Starts from Here


@receiver(post_save, sender=UserProfile)
def new_user_signup_email(sender, instance, created, **kwargs):
    if created:
        mail.send(
            recipients=instance.user.email,
            sender="no-reply@gamehunter.in",
            template="new_user_sign_up",
            priority="now",
            backend="django_ses",
            context={
                "user": instance
            },
        )
        return "Email Sent"
