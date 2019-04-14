from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from shop.models import Product, Plan, Blog


# Code Starts Below

def clear_product_list_view_cache():
    cache.delete_many(
        ["featured_playstation_games", "featured_xbox_games", "new_released_games", "new_arrived_products",
         "trending_products"])


@receiver(post_delete, sender=Product)
def product_post_delete_handler(sender, **kwargs):
    clear_product_list_view_cache()


@receiver(post_save, sender='shop.Product')
def product_post_save_handler(sender, **kwargs):
    print(cache.get("featured_playstation_games"))
    if kwargs["created"]:
        clear_product_list_view_cache()


def clear_blog_list_view_cache():
    cache.delete_many(["articles_list_view", "homepage_blogs"])


@receiver(post_delete, sender=Blog)
def blog_post_delete_handler(sender, **kwargs):
    clear_blog_list_view_cache()


@receiver(post_save, sender=Blog)
def blog_post_save_handler(sender, **kwargs):
    if kwargs["created"]:
        clear_blog_list_view_cache()
