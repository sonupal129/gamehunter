from django.contrib.sitemaps import Sitemap
from shop.models import Category, Plan, Product
from django.urls import reverse
# Start Working Below


class StaticViewSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ["shop:homepage", "shop:about-us", "shop:contact-us", "shop:privacy-policy", "shop:faq",
                "shop:shipping", "shop:subscription-list", "shop:sell-games"]

    def location(self, obj):
        return reverse(obj)


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

