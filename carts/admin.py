from django.contrib import admin
from .models import *


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "date", "user", "payment_status", "updated"]
    readonly_fields = (
        "cart_id", "date", "updated", "payment_request", "total_mrp", "total_selling_price", "total_discount",
        "address",
        "products", "user", "payment_id", "payment_status", "plan",)


class ProductOrdersAdmin(admin.ModelAdmin):
    list_display = ["suborder_id", "payment_method", "condition", "status", "order_date",]
    readonly_fields = (
        "suborder_id", "payment_method", "condition", "hunter_discount", "total_discount", "selling_price", "mrp",
        "final_selling_price", "delivery_charges", "product", "order_date", "address", "cart",)
    search_fields = ["suborder_id", "product"]
    list_filter = ["status", "condition", "payment_method"]


class SubscriptionOrdersAdmin(admin.ModelAdmin):
    list_display = ["suborder_id", "active", "order_date"]
    readonly_fields = ("suborder_id", "payment_method", "subscription_amount", "security_deposit",
                       "subscription_duration", "extra_month", "available_swaps", "order_date", "user", "expiry_date",
                       "address", "cart",)
    search_fields = ["suborder_id"]
    list_filter = ["active", "subscription_duration",]


admin.site.register(Cart, CartAdmin)
admin.site.register(ProductOrders, ProductOrdersAdmin)
admin.site.register(SubscriptionOrders, SubscriptionOrdersAdmin)
