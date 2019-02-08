from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import *
from django.http import HttpResponseRedirect
from .forms import CheckoutForm
from shop.models import Plan
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    item_list = cart_obj.total_items_list()
    cart_obj.total_mrp = cart_obj.get_mrp()
    cart_obj.total_selling_price = cart_obj.get_selling_price()
    cart_obj.save()
    return render(request, "carts/cart-page.html", {"carts": item_list, "cart": cart_obj})


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


def cart_remove_product(request, slug):
    prod_obj = Product.objects.get(slug=slug)
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.remove(prod_obj)
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def remove_whole_cart(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    cart_obj.products.clear()
    cart_obj.plan = None
    cart_obj.save()
    request.session["cart_items"] = cart_obj.total_cart_items_count()
    request.session["cart_total"] = int(cart_obj.get_selling_price())
    return redirect("carts:cart")


def cart_checkout(request):
    cart_obj, new_obj = Cart.objects.create_or_get_cart(request)
    checkout_form = CheckoutForm(request.POST or None)
    context = {
        "products": cart_obj.total_items_list(),
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


