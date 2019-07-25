from django.contrib import admin
from shop.models import *
from django.contrib.admin import ModelAdmin
from .csv_importer_exporter import *
from shop.debug import ExceptionLog
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

admin.site.site_header = 'Game Hunter Admin'
admin.site.site_title = 'Game Hunter Admin'


class AttributeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent',)


admin.site.register(Attribute, AttributeAdmin)


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent',)
    readonly_fields = ("slug",)


admin.site.register(Category, CategoryAdmin)


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ['file']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    fields = ['attribute', 'value']
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field is self.model.attribute.field:
            try:
                kwargs["queryset"] = Attribute.objects.get(
                    name="Product").get_children()
            except IndexError:
                print(
                    "PRODUCT attribute is not available in attribute Model, kindly add it with it's children ")
        return super(ProductAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('name', 'category', 'item_status', 'active')
    inlines = [ProductAttributeInline, PhotoInline]
    filter_horizontal = ('plan',)
    search_fields = ["name"]
    list_filter = ["item_status", "active",
                   "category", "condition", "is_featured"]
    actions = ["out_of_stock_selected_products", "in_stock_selected_products", "subscription_only_selected_products",
               "make_active_selected_products", "make_inactive_selected_products"]

    def save_model(self, request, obj, form, change):
        domain = request.META['HTTP_HOST']
        protocol = 'https'
        if settings.DEBUG:
            protocol = 'http'
        complete_domain = protocol + '://' + domain + '/'
        cache_keys_list = [complete_domain + "_homepage_products_lists", "new_released_games", "new_arrived_products",
                           "featured_playstation_games", "featured_xbox_games", "trending_products"]
        cache.delete_many(cache_keys_list)
        return super().save_model(request, obj, form, change)

    def out_of_stock_selected_products(self, request, queryset):
        queryset.update(item_status='O')
        return self.message_user(request, f"{queryset.count()} products marked out of stock")

    def in_stock_selected_products(self, request, queryset):
        queryset.update(item_status='I')
        return self.message_user(request, f"{queryset.count()} products marked in stock")

    def subscription_only_selected_products(self, request, queryset):
        queryset.update(item_status='S')
        return self.message_user(request, f"{queryset.count()} products marked subscription only")

    def make_active_selected_products(self, request, queryset):
        qs = queryset.filter(item_status__in=["I", "S"])
        qs.update(active=True)
        return self.message_user(request, f"{qs.count()} products marked active")

    def make_inactive_selected_products(self, request, queryset):
        queryset.update(active=False)
        print(len(connection.queries))
        return self.message_user(request, f"{queryset.count()} products marked inactive")

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscription_amount',
                    'security_deposit', "active")
    fields = ['name', 'type', 'duration', 'additional_month', 'swaps', 'description', 'active',
              ('subscription_amount', 'security_deposit', 'refundable', 'discount'),
              'term_condition',
              ('image', 'image1')]

    def save_model(self, request, obj, form, change):
        cache.delete("game_hunter_rental_plan_list")
        return super().save_model(request, obj, form, change)


class PromoCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'promocard_type', 'active')
    inlines = [PhotoInline]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed')
    raw_id_fields = ['user']


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'phone_number')
    raw_id_fields = ['user']


class BrandAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'image',
              ('is_developer', 'is_publisher', 'is_manufacturer')]
    search_fields = ["name"]
    list_display = ["name", "is_developer", "is_publisher", "is_manufacturer"]
    list_filter = ["is_developer", "is_publisher", "is_manufacturer"]


class CSVImporterAdmin(ModelAdmin):
    list_display = ["data_type", "path", "date"]
    fields = ["data_type", "path"]
    actions = ['upload_or_update_data']

    def upload_or_update_data(self, request, queryset):
        message = ""
        for q in queryset:
            file_path = q.path.path
            if q.data_type == "PD":
                message = upload_products(file_path)
            else:
                message = "Invalid Data Type"
        return self.message_user(request, message)


class ExceptionAdmin(ModelAdmin):
    list_display = ["views", "message", "timestamp"]
    readonly_fields = ("views", "message", "timestamp", "exceptionclass",)


admin.site.register(CSVImporter, CSVImporterAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(PromoCard, PromoCardAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Genre)
admin.site.register(Product, ProductAdmin)
admin.site.register(ExceptionLog, ExceptionAdmin)

