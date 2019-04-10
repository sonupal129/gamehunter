from shop.models import Product, ProductAttribute, Attribute
from carts.models import Cart
from django.utils import timezone
import datetime
from carts.models import Cart
# Start Writing Functions Below


def update_pay_per_game_product_price():
    """This function run as task, where it checks all products, and update pay per game price of product which
    has/has not game based plan"""

    attr = Attribute.objects.get(attribute="game_based_plan_price")
    products = Product.objects.filter(active=True, item_status__in=["I", "S"])
    for product in products:
        if product.plan.filter(type="GB"):
            game_price_attribute = ProductAttribute.objects.filter(product=product, attribute=attr).first()
            if game_price_attribute:
                if product.mrp <= 1499:
                    game_price_attribute.value = 300
                elif product.mrp > 1500 < 4000:
                    game_price_attribute.value = 500
                else:
                    del game_price_attribute
                game_price_attribute.save()
            else:
                if product.mrp <= 1499:
                    subscription_game_price = ProductAttribute(attribute=attr, value=300, product=product)
                elif product.mrp > 1500 < 4000:
                    subscription_game_price = ProductAttribute(attribute=attr, value=500, product=product)
                else:
                    pass
                subscription_game_price.save()
        else:
            game_price_attribute = ProductAttribute.objects.filter(product=product, attribute=attr)
            if game_price_attribute:
                del game_price_attribute
    return "All Products Pay Per Price Been Updated!"

