from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView, ListView
from carts.models import *
from carts.emails import send_cart_order_place_email
import requests
from carts.tasks import create_order
from django.http import HttpResponseRedirect, HttpResponse
from carts.forms import CheckoutForm
from shop.models import Plan
from django.core.exceptions import ObjectDoesNotExist
from gamehunter.settings import INSTAMOJO_API_KEY, INSTAMOJO_AUTH_TOKEN, BASE_PAYMENT_URL, PAYEMENT_REDIRECT_URL
# Create your views here.


def cart_home(request):
    context = {}
    if request.session.get("cart_error", None):
        context["error"] = request.session["cart_error"]
        del request.session["cart_error"]
    else:
        pass
    cart_obj = Cart.objects.create_or_get_cart(request)
    products, pay_game_products = cart_obj.total_items_list()
    context["products"] = products
    context["pay_game_products"] = pay_game_products
    cart_obj.total_mrp = cart_obj.get_mrp()
    cart_obj.total_selling_price = cart_obj.get_selling_price()
    cart_obj.save()
    context["cart"] = cart_obj
    return render(request, "carts/cart-page.html", context)


def cart_add_plan(request, slug):
    plan_obj = Plan.objects.get(slug=slug)
    cart_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.plan = plan_obj
    cart_obj.save(update_fields=["plan"])
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove_plan(request, slug):
    plan_obj = Plan.objects.get(slug=slug)
    cart_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.plan = None
    cart_obj.save(update_fields=["plan"])
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def cart_add_product(request, slug):
    prod_obj = Product.objects.get(slug=slug)
    prod_obj.add_to_trending_products()
    cart_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.add(prod_obj)
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_pay_per_game_product(request, slug):
    product = Product.objects.get(slug=slug)
    product.add_to_trending_products()
    plan = product.plan.filter(type="GB").first()
    cart_obj = Cart.objects.create_or_get_cart(request)
    if cart_obj.pay_game_products.all():
        cart_obj.pay_game_products.clear()
        cart_obj.pay_game_products.add(product)
    else:
        cart_obj.pay_game_products.add(product)
    return redirect(plan)


def cart_remove_product(request, slug):
    prod_obj = Product.objects.get(slug=slug)
    cart_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.remove(prod_obj)
    cart_obj.pay_game_products.remove(prod_obj)
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def remove_whole_cart(request):
    cart_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.clear()
    cart_obj.pay_game_products.clear()
    cart_obj.plan = None
    cart_obj.save()
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def cart_checkout(request):
    headers = {"X-Api-Key": INSTAMOJO_API_KEY, "X-Auth-Token": INSTAMOJO_AUTH_TOKEN}
    try:
        cart_obj = Cart.objects.get(cart_id=request.session.get("cart_id"))
    except Cart.DoesNotExist:
        return redirect("shop:homepage")
    checkout_form = CheckoutForm(request.POST or None)
    products, pay_game_products = cart_obj.total_items_list()
    if cart_obj.plan:
        if cart_obj.plan.type == "GB" and pay_game_products is None:
            request.session["cart_error"] = "Please Add Product in Cart"
            return redirect("carts:cart")
        elif cart_obj.plan.type == "SB" and pay_game_products:
            request.session["cart_error"] = "Please Choose Pay Game Plan"
            return redirect("carts:cart")
        else:
            pass
    else:
        if pay_game_products:
            request.session["cart_error"] = "Please Add Pay Game Plan in Cart"
            return redirect("carts:cart")
        else:
            pass
    context = {
        "products": products,
        "pay_game_products": pay_game_products,
        "cart": cart_obj,
        "form": checkout_form
    }
    if checkout_form.is_valid():
        user = request.user
        if not user.first_name:
            user.first_name = checkout_form.cleaned_data.get("first_name")
            user.last_name = checkout_form.cleaned_data.get("last_name")
            user.save(update_fields=["first_name", "last_name"])

        if not user.userprofile.phone_number:
            user.userprofile.phone_number = checkout_form.cleaned_data.get("mobile")
            user.userprofile.save(update_fields=["phone_number"])

        address_obj = Address.objects.create(user=user.userprofile)
        address_obj.phone_number = checkout_form.cleaned_data.get("mobile")
        address_obj.address = checkout_form.cleaned_data.get("shipping_address")
        address_obj.city = checkout_form.cleaned_data.get("city")
        address_obj.state = checkout_form.cleaned_data.get("state")
        address_obj.save()
        cart_obj.address = address_obj
        cart_obj.save()
        if user.is_authenticated and user.is_active:
            payload = {"purpose": cart_obj.cart_id,
                   "amount": str(cart_obj.get_selling_price()),
                   "buyer_name": cart_obj.user.first_name,
                   "email": cart_obj.user.email,
                   "phone": str(cart_obj.user.userprofile.phone_number),
                   "redirect_url": PAYEMENT_REDIRECT_URL,
                   "send_email": False,
                   "send_sms": False,
                   }
        response = requests.post(BASE_PAYMENT_URL, data=payload, headers=headers)
        if response:
            payment_detail = response.json()["payment_request"]
            cart_obj.payment_request = payment_detail
            cart_obj.save(update_fields=["payment_request"])
            embeded_url = str(payment_detail.get("longurl") + str("?embed=form"))
            return HttpResponse("<script src='https://js.instamojo.com/v1/checkout.js'></script><script>Instamojo.open('{0}');</script>".format(embeded_url))
        return redirect("carts:checkout")
    else:
        CheckoutForm()
    return render(request, "carts/checkout.html", context)

def redirect_payment_complete(request):
    """ function takes request as argument and after receiving payment confirmation from payment gateway it redirect to
    payment complete or declined page"""
    user = request.user
    cart_id = request.session.get("cart_id")
    try:
        cart_obj = Cart.objects.get(cart_id=cart_id)
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
                if get_payment_status == "Credit" and cart_obj.payment_request and get_payment_id:
                    send_cart_order_place_email(cart_obj.id)
                    cart_obj.payment_id = get_payment_id
                    cart_obj.payment_status = get_payment_status
                    cart_obj.save(update_fields=["payment_id", "payment_status"])
                    create_order(cart_obj.id)
                    del request.session["cart_id"]
                    del request.session["cart_items"]
                    del request.session["cart_total"]
                    request.session.modified = True
                    return render(request, "carts/transaction-successful.html", context)
                else:
                    return render(request, "carts/transaction-declined.html", context)
            return redirect("carts:cart")
    return redirect("shop:login")

class TestView(TemplateView):
    template_name = "shop/coming-soon.html"
