from post_office import mail
from django.dispatch import receiver
from shop.models import UserProfile
from django.db.models.signals import pre_save, post_save
# Testing
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, force_bytes
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


def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id)).decode()
    domain = request.META["HTTP_HOST"]
    mail.send(
        recipients=user.email,
        sender="no-reply@gamehunter.in",
        template="password_reset_template",
        priority="now",
        backend="django_ses",
        context={
            "user": user.email,
            "token": token,
            "uid": uid,
            "domain": domain,
        },
    )
    return "Email Sent"
