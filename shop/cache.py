from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from shop.models import Product, Plan, Blog


# Code Starts Below

def clear_product_list_view_cache():
    cache.delete("featured_playstation_games")
    cache.delete("featured_xbox_games")
    cache.delete("new_released_games")
    cache.delete("new_arrived_products")
    cache.delete("products_list_view")
    cache.delete("side_list_products")


@receiver(post_delete, sender=Product)
def product_post_delete_handler():
    clear_product_list_view_cache()


@receiver(post_save, sender=Product)
def product_post_save_handler():
    clear_product_list_view_cache()


def clear_blog_list_view_cache():
    cache.delete("articles_list_view")
    cache.delete("homepage_blogs")


@receiver(post_delete, sender=Blog)
def blog_post_delete_handler():
    clear_blog_list_view_cache()


@receiver(post_save, sender=Blog)
def blog_post_save_handler():
    clear_blog_list_view_cache()


def clear_plan_list_view_cache():
    cache.delete("plan_list_views")


@receiver(post_delete, sender=Plan)
def plan_post_delete_handler():
    clear_plan_list_view_cache()


@receiver(post_save, sender=Plan)
def plan_post_save_handler():
    clear_plan_list_view_cache()

