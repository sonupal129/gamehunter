from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from shop.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import *
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.generic import TemplateView
from shop.emails import send_password_reset_email
# Started Working Below


app_name = 'shop'

sitemaps = {
    "categories": CategorySiteMap,
    "plans": PlanSiteMap,
    "products": ProductSiteMap,
    "static": StaticViewSiteMap,
}

urlpatterns = [
#     Robots.txt urls
    path('robots.txt/', TemplateView.as_view(template_name="shop/robots.txt", content_type='text/plain'),
         name='robots'),
#     Cache Clearing urls
    path('cache/clear', clear_cache, name='clear-cache'),
#     Sitemaps urls
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
    
    path('', HomePageView.as_view(), name='homepage'),
    # path('consoles/', views.ProductListView.as_view(), name='consoles'),
    # path('gaming-accessories/', views.ProductListView.as_view(), name='gaming-accessories'),
#     Static pages urls
    path('about-us/', cache_page(86400)(AboutUsView.as_view()), name='about-us'),
    path('privacy-policy/', cache_page(86400)(PrivacyPolicyView.as_view()), name='privacy-policy'),
    path('return-cancellation/', cache_page(86400)(ReturnCancellationView.as_view()), name='return-cancellation'),
    path('shipping/', cache_page(86400)(ShipplingPolicyView.as_view()), name='shipping'),
    path('faq/', cache_page(86400)(FaqView.as_view()), name='faq'),
    path('term-condition/', cache_page(86400)(TermConditionView.as_view()), name='term-condition'),
    path('coming-soon/', cache_page(86400)(ComingSoonView.as_view()), name='coming-soon'),
#    User Accounts Urls
    path('login/', login_register_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-orders/', login_required(MyOrderView.as_view()), name='orders'),
    path('my-orders/<str:cart>/', OrderDetailView.as_view(), name='order-details'),
    path('my-account/', login_required(MyAccountView.as_view()), name='my-account'),
    path('password-reset/', reset_password, name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="shop/registrations/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="shop/registrations/password_reset_confirm.html",
                                                     success_url=reverse_lazy("shop:password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="shop/registrations/password_reset_complete.html"),
         name='password_reset_complete'),
# Products Urls
    path('subscription-plans/', SubscriptionPlanView.as_view(), name='subscription-list'),
    path('search/', ProductListView.as_view(), name='search'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('products/<path:slug>/', ProductListView.as_view(), name='product-list'),
    
    path('subscription-plans/<slug:slug>', SubscriptionDetailView.as_view(), name='subscription-detail'),
# Contact Urls
    path('sell-ur-games/', SellYourGamesView.as_view(), name='sell-games'),
    path('contact-us/', cache_page(86400)(ContactUsView.as_view()), name='contact-us'),
# Testing Urls
    path('test/', test_view, name='test'),
]