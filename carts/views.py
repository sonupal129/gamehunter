from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView, ListView
from .models import *
from django.http import HttpResponseRedirect
from .forms import CheckoutForm
from shop.models import Plan
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    products, pay_game_products = cart_obj.total_items_list()
    cart_obj.total_mrp = cart_obj.get_mrp()
    cart_obj.total_selling_price = cart_obj.get_selling_price()
    cart_obj.save()
    print(products)
    print(pay_game_products)
    return render(request, "carts/cart-page.html",
                  {"products": products, "cart": cart_obj, "pay_game_products": pay_game_products})


def cart_add_plan(request, slug):
    plan_obj = Plan.objects.get(slug=slug)
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.plan = plan_obj
    cart_obj.save(update_fields=["plan"])
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove_plan(request, slug):
    plan_obj = Plan.objects.get(slug=slug)
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.plan = None
    cart_obj.save(update_fields=["plan"])
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def cart_add_product(request, slug):
    prod_obj = Product.objects.get(slug=slug)
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.add(prod_obj)
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    print(int(cart_obj.get_selling_price()))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_pay_per_game_product(request, slug):
    product = Product.objects.get(slug=slug)
    plan = product.plan.filter(type="GB").first()
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    context = {}
    if not request.user.userprofile.has_subscription():
        if cart_obj.pay_game_products.all().count() == 0:
            print(request.user)
            cart_obj.pay_game_products.add(product)
        else:
            return redirect(product, {"error": "Rajus"})
    return redirect(plan)


def cart_remove_product(request, slug):
    prod_obj = Product.objects.get(slug=slug)
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.remove(prod_obj)
    cart_obj.pay_game_products.remove(prod_obj)
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def remove_whole_cart(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.clear()
    cart_obj.pay_game_products.clear()
    cart_obj.plan = None
    cart_obj.save()
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def cart_checkout(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    checkout_form = CheckoutForm(request.POST or None)
    products, pay_game_products = cart_obj.total_items_list()
    if cart_obj.plan:
        if cart_obj.plan.type == "GB" and pay_game_products is None:
            return redirect("carts:cart")
        elif cart_obj.plan.type == "SB" and pay_game_products:
            return redirect("carts:cart")
        else:
            pass
    else:
        if pay_game_products:
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
        return redirect("carts:payment")
    else:
        CheckoutForm()
    return render(request, "carts/checkout.html", context)


class TestView(TemplateView):
    template_name = "shop/coming-soon.html"
