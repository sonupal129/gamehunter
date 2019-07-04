from django.contrib import admin
from news.models import *
from mptt.admin import DraggableMPTTAdmin

# Register your models here.

class NewsCategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent',)
    readonly_fields = ("slug",)

admin.site.register(NewsCategory, NewsCategoryAdmin)

class NewsAttributeInline(admin.TabularInline):
    model = NewsAttribute
    extra = 1
    fields = ["attribute", "value"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field is self.model.attribute.field:
            try:
                kwargs["queryset"] = Attribute.objects.get(
                    attribute="Blogs").get_children()
            except IndexError:
                print(
                    "BLOG attribute is not available in attribute Model, kindly add it with it's children ")
        return super(BlogAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class NewsAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'date_created', 'status',)
    inlines = [NewsAttributeInline]
    search_fields = ("title",)
    list_filter = ("status",)

admin.site.register(News, NewsAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user",)
    

admin.site.register(Author, AuthorAdmin)