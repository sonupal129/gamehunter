from django_slack import slack_message
from carts.models import ProductOrders, Cart, SubscriptionOrders
from carts.signals import new_order_received, new_subscription_order_received
from django.dispatch import receiver

# Code Starts from Here


@receiver(new_order_received)
def new_product_order_received(sender, **kwargs):
    suborder = kwargs.get("suborder")
    if suborder:
        context = {
            "order": suborder,
        }
        slack_message("carts/slack-message/new-order-received.html", context)
    return ""


@receiver(new_subscription_order_received)
def new_subscription_order_received(sender, **kwargs):
    subscription = kwargs.get("suborder")
    if subscription:
        context = {
            "subscription": subscription
        }
        slack_message("carts/slack-message/new-subscription-order-received.html", context)
    return ""
