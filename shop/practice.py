import csv
import datetime
from shop.models import Product, Attribute
from carts.models import Cart


def total_products_in_cart(*args):
    for cart in args:
        if cart.products.all():
            for p in cart.products.all():
                p.add_to_trending_products()
        if cart.pay_game_products.all():
            for p in cart.pay_game_products.all():
                p.add_to_trending_products()
    return "All Products Clicks Added"
