from django_slack import slack_message
# from carts.models import ProductOrders, Cart, SubscriptionOrders
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from background_task import background
# Code Starts from Here


def new_product_order_received(product_order):
    if product_order:
        context = {
            "order": product_order
        }
    return slack_message("carts/slack-message/new-order-received.html", context)


# @receiver(post_save, sender=SubscriptionOrders)
# def new_subscription_order_received(sender, instance, created, **kwargs):
#     if created:
#         context = {
#             "subscription": instance
#         }
#     return slack_message("carts/slack-message/new-subscription-order-received.html", context)
