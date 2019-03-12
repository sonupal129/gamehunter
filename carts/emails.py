from carts.models import *
from post_office import mail
from carts.signals import order_payment_received, new_user_profile_created
from django.dispatch import receiver

# Code Starts from Here


@receiver(order_payment_received)
def send_cart_order_place_email(sender, **kwargs):
    # cart = Cart.objects.get(id=13)
    # print(cart)
    # print(cart.total_items_list())
    cart = kwargs.get("cart_id")
    print(cart.user.email)
    if cart.payment_status == "Credit":
        mail.send(
            recipients=cart.user.email,
            sender="no-reply@gamehunter.in",
            template="new_order_received",
            priority="now",
            backend="django_ses",
            context={
                "products": cart.total_items_list(),
                "cart": cart,

            },
        )
        return ""


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
