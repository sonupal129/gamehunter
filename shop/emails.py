from carts.models import *
from post_office import mail
from carts.signals import order_payment_received, new_user_profile_created
from django.dispatch import receiver
# Code Starts from Here


@receiver(new_user_profile_created)
def new_user_signup_email(sender, **kwargs):
    user = kwargs.get("user")
    mail.send(
        recipients=user.email,
        sender="no-reply@gamehunter.in",
        template="new_user_sign_up",
        priority="now",
        backend="django_ses",
        context={
            "user": user
        },
    )
    return ""
