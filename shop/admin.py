from django.contrib import admin
from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import *
from django.contrib.admin import ModelAdmin
from .csv_importer_exporter import *
from shop.debug import ExceptionLog

# Register your models here.

admin.site.site_header = 'Game Hunter Admin';
admin.site.site_title = 'Game Hunter Admin';


class AttributeAdmin(TreeAdmin):
    form = movenodeform_factory(Attribute, exclude='slug')


admin.site.register(Attribute, AttributeAdmin)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category, exclude='slug')
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
                kwargs["queryset"] = Attribute.objects.get(attribute="Product").get_children()
            except IndexError:
                print("PRODUCT attribute is not available in attribute Model, kindly add it with it's children ")
        return super(ProductAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('name', 'category', 'item_status', 'active')
    inlines = [ProductAttributeInline, PhotoInline]
    filter_horizontal = ('plan',)
    search_fields = ["name"]
    list_filter = ["item_status", "active", "category", "condition"]
    actions = ["out_of_stock_selected_products", "in_stock_selected_products", "subscription_only_selected_products",
               "make_active_selected_products", "make_inactive_selected_products"]

    def out_of_stock_selected_products(self, request, queryset):
        count = 0
        for q in queryset:
            q.item_status = 'O'
            count += 1
            q.save()
        return self.message_user(request, f"{count} products marked out of stock")

    def in_stock_selected_products(self, request, queryset):
        count = 0
        for q in queryset:
            q.item_status = 'I'
            count += 1
            q.save()
        return self.message_user(request, f"{count} products marked in stock")

    def subscription_only_selected_products(self, request, queryset):
        count = 0
        for q in queryset:
            q.item_status = 'S'
            count += 1
            q.save()
        return self.message_user(request, f"{count} products marked subscription only")

    def make_active_selected_products(self, request, queryset):
        count = 0
        for q in queryset:
            if q.item_status == "I" or q.item_status == "S":
                q.active = True
                count += 1
                q.save()
        return self.message_user(request, f"{count} products marked active")

    def make_inactive_selected_products(self, request, queryset):
        count = 0
        for q in queryset:
            q.active = False
            count += 1
            q.save()
        return self.message_user(request, f"{count} products marked inactive")


class BlogAttributeInline(admin.TabularInline):
    model = BlogAttribute
    fields = ['attribute', 'value']
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field is self.model.attribute.field:
            try:
                kwargs["queryset"] = Attribute.objects.get(attribute="Blogs").get_children()
            except IndexError:
                print("BLOG attribute is not available in attribute Model, kindly add it with it's children ")
        return super(BlogAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BlogAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'date_created', 'status',)
    inlines = [BlogAttributeInline]
    raw_id_fields = ['product']
    search_fields = ("title",)
    list_filter = ("status", "blog_type",)

admin.site.register(Blog, BlogAdmin)


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscription_amount', 'security_deposit')
    fields = ['name', 'type', 'duration', 'additional_month', 'swaps', 'description', 'active',
              ('subscription_amount', 'security_deposit', 'refundable', 'discount'),
              'term_condition',
              ('image', 'image1')]


class PromoCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'active')
    inlines = [PhotoInline]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed')
    raw_id_fields = ['user']


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'phone_number')
    raw_id_fields = ['user']


class BrandAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'image', ('is_developer', 'is_publisher', 'is_manufacturer')]
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
