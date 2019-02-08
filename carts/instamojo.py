from carts.forms import CheckoutForm
from carts.models import Cart, SubscriptionOrders
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from carts.signals import order_payment_received
from django.dispatch import receiver
from gamehunter.settings import INSTAMOJO_API_KEY, INSTAMOJO_AUTH_TOKEN
# Code Starts from Below

headers = {"X-Api-Key": INSTAMOJO_API_KEY, "X-Auth-Token": INSTAMOJO_AUTH_TOKEN}


def send_payment_request(request):
    """" This funcation takes request as argument and send payment request instamojo server after receiving
    successful url from instamojo it redirect to their server or to checkout page"""
    user = request.user
    if user.is_authenticated and user.is_active:
        cart_obj = Cart.objects.get(cart_id=request.session.get("cart_id"))
        payload = {"purpose": cart_obj.cart_id,
                   "amount": str(cart_obj.get_selling_price()),
                   "buyer_name": cart_obj.user.first_name,
                   "email": cart_obj.user.email,
                   "phone": str(cart_obj.user.userprofile.phone_number),
                   "redirect_url": "http://127.0.0.1:8000/cart/payment/successful",
                   }
        response = requests.post("https://test.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
        if response:
            payment_detail = response.json()["payment_request"]
            cart_obj.payment_request = payment_detail
            cart_obj.save(update_fields=["payment_request"])
            return redirect(payment_detail.get("longurl") + str("?embed=form"))
        else:
            return redirect("carts:checkout")
    return redirect("shop:login")


def redirect_payment_complete(request):
    """ function takes request as argument and after receiving payment confirmation from payment gateway it redirect to
    payment complete or declined page"""
    user = request.user
    try:
        cart_obj = Cart.objects.get(cart_id=request.session.get("cart_id"))
    except:
        pass
    else:
        if user.is_authenticated and user.is_active:
            if cart_obj:
                get_payment_id = request.GET.get("payment_id", "")
                get_payment_status = request.GET.get("payment_status", "")

                context = {
                    "cart": cart_obj,
                }
                if get_payment_status == "Credit" and get_payment_id:
                    cart_obj.payment_id = get_payment_id
                    cart_obj.payment_status = get_payment_status
                    cart_obj.save(update_fields=["payment_id", "payment_status"])
                    order_payment_received.send(sender=Cart, cart_id=cart_obj,
                                                payment_status=cart_obj.payment_status)
                    del request.session["cart_id"]
                    del request.session["cart_items"]
                    del request.session["cart_total"]
                    request.session.modified = True
                    return render(request, "carts/transaction-successful.html", context)
                else:
                    return render(request, "carts/transaction-declined.html", context)
            return redirect("carts:cart")
    return redirect("shop:login")


@receiver(order_payment_received)
def create_order(sender, **kwargs):
    cart = kwargs.get("cart_id")
    print(sender)
    print(kwargs.get("cart_id"))
    cart.create_product_orders()
    if cart.plan:
        cart.create_subscription_order()
