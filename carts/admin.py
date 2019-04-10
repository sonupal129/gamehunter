from django.contrib import admin
from .models import *


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "date", "user", "payment_status", "updated", "order_payment_request"]
    readonly_fields = (
        "cart_id", "date", "updated", "payment_request", "total_mrp", "total_selling_price", "total_discount",
        "address",
        "products", "user", "payment_id", "payment_status", "plan", "pay_game_products",)
    list_filter = ["payment_status", "date"]

    def order_payment_request(self, obj):
        if obj.payment_request:
            return True
        else:
            return False
    order_payment_request.boolean = True


class ProductOrdersAdmin(admin.ModelAdmin):
    list_display = ["suborder_id", "payment_method", "condition", "status", "order_date", "cart"]
    readonly_fields = (
        "suborder_id", "payment_method", "condition", "hunter_discount", "total_discount", "selling_price", "mrp",
        "final_selling_price", "delivery_charges", "product", "order_date", "address", "cart",)
    search_fields = ["suborder_id"]
    list_filter = ["status", "condition", "payment_method"]


class SubscriptionOrdersAdmin(admin.ModelAdmin):
    list_display = ["suborder_id", "active", "order_date", "cart"]
    readonly_fields = ("suborder_id", "payment_method", "subscription_amount", "security_deposit",
                       "subscription_duration", "extra_month", "available_swaps", "order_date", "user", "expiry_date",
                       "address", "cart", "type",)
    search_fields = ["suborder_id"]
    list_filter = ["active", "subscription_duration",]


admin.site.register(Cart, CartAdmin)
admin.site.register(ProductOrders, ProductOrdersAdmin)
admin.site.register(SubscriptionOrders, SubscriptionOrdersAdmin)
