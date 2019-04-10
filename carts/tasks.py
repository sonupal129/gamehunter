from shop.models import Product, ProductAttribute, Attribute
from carts.models import Cart
from django.utils import timezone
import datetime
from carts.models import Cart
from carts.emails import *
from background_task import background
from background_task.models import Task
# Start Writing Functions Below


def delete_old_cart():
    """This function runs as task, Where it checks all carts and carts which are older than 45 days without user details and
    carts which are older than 90 days with no user activity get deleted from system"""
    one_half_month_old = Cart.objects.filter(user=None, payment_status="", products=None, payment_request="", plan=None,
                                             updated__lte=timezone.now() - datetime.timedelta(45))
    if one_half_month_old:
        one_half_month_old.delete()
    four_month_old = Cart.objects.filter(payment_status=None, payment_request=None, updated__lte=timezone.now() - datetime.timedelta(120))
    if four_month_old:
        four_month_old.delete()
    return "Carts which were older than 45 and 90 days deleted from system"


def send_cart_dropout_email(request):
    """This Function create emails in django post office for user who dropped out their cart"""
    yesterday = timezone.now() - datetime.timedelta(1)
    carts = Cart.objects.filter(user__isnull=False, payment_request=None, payment_status=None,
                                date__range=[yesterday - datetime.timedelta(10), yesterday])[:5]
    for cart in carts:
        if cart.products:
            email_to_user_added_products(cart)
        elif cart.pay_game_products:
            email_to_user_added_pay_per_game_products(cart)
        elif cart.plan:
            email_to_user_added_plan_in_cart(cart)
        else:
            pass
    return "Email Task Ran Successfully"


# Calling Functions
# if "raju" == "raju":

