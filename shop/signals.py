from django.dispatch import Signal
from django.db.models.signals import m2m_changed, post_save
from shop.models import Product, ProductAttribute, Attribute
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import request_finished
from shop.models import ProductAttribute
# Code Starts from Here


@receiver(m2m_changed, sender=Product.plan.through)
def add_delete_pay_per_game_price(sender, instance, **kwargs):
    """This Signal function update pay per game price based on product mrp"""
    attr = Attribute.objects.get(name="game_based_plan_price")
    action = kwargs.get("action")
    if instance and action == "pre_remove":
        if instance.plan.filter(type="GB", id__in=kwargs.get("pk_set")):
            ProductAttribute.objects.filter(product=instance, attribute=attr).delete()
        else:
            pass
    elif instance and action == "post_add":
        if instance.plan.filter(type="GB", id__in=kwargs.get("pk_set")):
            game_price_attribute = ProductAttribute.objects.filter(product=instance, attribute=attr).first()
            if game_price_attribute:
                if instance.mrp <= 1499:
                    game_price_attribute.value = 300
                    game_price_attribute.save()
                elif 1500 < instance.mrp < 4000:
                    game_price_attribute.value = 500
                    game_price_attribute.save()
                else:
                    del game_price_attribute
            else:
                if instance.mrp <= 1499:
                    ProductAttribute.objects.create(attribute=attr, value=300, product=instance)
                elif 1500 < instance.mrp < 4000:
                    ProductAttribute.objects.create(attribute=attr, value=500, product=instance)
                else:
                    pass
    return "Game Price Attribute Create or Deleted"


@receiver(post_save, sender=Product)
def update_pay_per_game_price(sender, instance, **kwargs):
    attr = Attribute.objects.get(name="game_based_plan_price")
    if instance.get_pay_per_game_subscription_price():
        obj = instance.get_pay_per_game_subscription_price()
        if instance.mrp <= 1499:
            obj.value = 300
            obj.save()
        elif 1500 < instance.mrp < 4000:
            obj.value = 500
            obj.save()
        else:
            ProductAttribute.objects.filter(product=instance, attribute=attr).delete()
    return "Game Price Attribute Updated"


@receiver(post_save, sender=Product)
def create_product_redirect_url(sender, instance, created, **kwargs):
    site = Site.objects.get(id=settings.SITE_ID)
    attr = Attribute.objects.get(name="old_slug")
    old_slug = instance.get_old_slug()
    if created:
        ProductAttribute.objects.create(attribute=attr, value=instance.slug, product=instance)
    else:
        if old_slug:
            if old_slug.value != instance.slug:
                Redirect.objects.create(site=site, old_path="/" + old_slug.value, new_path="/" + instance.slug)
                old_slug.value = instance.slug
                old_slug.save()
        else:
            ProductAttribute.objects.create(attribute=attr, value=instance.slug, product=instance)
    return "Redirect Url Created"

