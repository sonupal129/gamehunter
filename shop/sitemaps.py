from django.contrib.sitemaps import Sitemap
from shop.models import Blog, Category, Plan, Product
from django.urls import reverse
# Start Working Below


class StaticViewSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ["shop:homepage", "shop:articles", "shop:about-us", "shop:contact-us", "shop:privacy-policy", "shop:faq",
                "shop:shipping", "shop:subscription-list", "shop:sell-games"]

    def location(self, obj):
        print(obj)
        return reverse(obj)


class BlogSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(status="P").order_by("-date")


class CategorySiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.4
    protocol = 'https'

    def items(self):
        return Category.objects.all()


class PlanSiteMap(Sitemap):
    changefreg = "monthly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Plan.objects.filter(active=True)


class ProductSiteMap(Sitemap):
    changefreg = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Product.objects.filter(active=True)

