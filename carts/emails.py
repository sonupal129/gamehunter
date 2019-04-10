from carts.models import *
from post_office import mail
from carts.signals import order_payment_received
from django.dispatch import receiver
from django.utils import timezone
import datetime
# Code Starts from Here


@receiver(order_payment_received)
def send_cart_order_place_email(sender, **kwargs):
    # cart = Cart.objects.get(id=13)
    # print(cart)
    # print(cart.total_items_list())
    cart = kwargs.get("cart_id")
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
                "user_name": cart.user.first_name + cart.user.last_name

            },
        )
        return ""

# Cart Drop Out Emails


def email_to_user_added_products(cart):
    mail.send(
        recipients=cart.user.email,
        sender="no-reply@gamehunter.in",
        backend="django_ses",
        priority="medium",
        scheduled_time=datetime.datetime.now()+datetime.timedelta(hours=11),
        context={
            "products": cart.products.all(),
            "last_visit": cart.updated,
            "user_name": cart.user.first_name + cart.user.last_name
            }
    )
    return ""


def email_to_user_added_pay_per_game_products(cart):
    mail.send(
        recipients=cart.user.email,
        sender="no-reply@gamehunter.in",
        backend="django_ses",
        priority="medium",
        scheduled_time=datetime.datetime.now() + datetime.timedelta(hours=10),
        context={
            "products": cart.pay_game_products.all(),
            "last_visit": cart.updated,
            "user_name": cart.user.first_name + cart.user.last_name
        },
    )


def email_to_user_added_plan_in_cart(cart):
    mail.send(
        recipients=cart.user.email,
        sender="no-reply@gamehunter.in",
        backend="django_ses",
        priority="medium",
        scheduled_time=datetime.datetime.now() + datetime.timedelta(hours=9),
        context={
            "plan": cart.plan,
            "last_visit": cart.updated,
            "user_name": cart.user.first_name + cart.user.last_name
        },
    )
