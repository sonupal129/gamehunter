from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shop.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import *
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Started Working Below


app_name = 'shop'

sitemaps = {
    "blogs": BlogSiteMap,
    "categories": CategorySiteMap,
    "plans": PlanSiteMap,
    "products": ProductSiteMap,
    "static": StaticViewSiteMap,
}

urlpatterns = [
    path('cache/clear', clear_cache, name='clear-cache'),
    path('url-optimize/sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('url-optimize/sitemap-<section>.xml', (sitemap_views.sitemap), {'sitemaps': sitemaps}, name='sitemaps'),
    path('', HomePageView.as_view(), name='homepage'),
    # path('consoles/', views.ProductListView.as_view(), name='consoles'),
    # path('gaming-accessories/', views.ProductListView.as_view(), name='gaming-accessories'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('about-us/', cache_page(86400)(AboutUsView.as_view()), name='about-us'),
    path('contact-us/', cache_page(86400)(ContactUsView.as_view()), name='contact-us'),
    path('privacy-policy/', cache_page(86400)(PrivacyPolicyView.as_view()), name='privacy-policy'),
    path('return-cancellation/', cache_page(86400)(ReturnCancellationView.as_view()), name='return-cancellation'),
    path('shipping/', cache_page(86400)(ShipplingPolicyView.as_view()), name='shipping'),
    path('faq/', cache_page(86400)(FaqView.as_view()), name='faq'),
    path('term-condition/', cache_page(86400)(TermConditionView.as_view()), name='term-condition'),
    path('login/', login_register_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('subscription-plans/', SubscriptionPlanView.as_view(), name='subscription-list'),
    path('articles/<slug:slug>', ArticleDetailView.as_view(), name='article-detail'),
    path('search/', ProductSearchView.as_view(), name='search'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('products/<path:slug>/', ProductListView.as_view(), name='product-list'),
    path('subscription-plans/<slug:slug>', SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('my-orders/', login_required(MyOrderView.as_view()), name='orders'),
    path('coming-soon/', ComingSoonView.as_view(), name='coming-soon'),
    path('my-account/', login_required(MyAccountView.as_view()), name='my-account'),
    path('sell-ur-games/', SellYourGamesView.as_view(), name='sell-games'),
    #     Password Change Urls
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

]