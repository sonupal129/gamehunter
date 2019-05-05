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
    "blogs": BlogSiteMap,
    "categories": CategorySiteMap,
    "plans": PlanSiteMap,
    "products": ProductSiteMap,
    "static": StaticViewSiteMap,
}

urlpatterns = [
    path('robots.txt/', TemplateView.as_view(template_name="shop/robots.txt", content_type='text/plain'),
         name='robots'),
    path('cache/clear', clear_cache, name='clear-cache'),
    path('url-optimize/sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('url-optimize/sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
    path('', HomePageView.as_view(), name='homepage'),
    # path('consoles/', views.ProductListView.as_view(), name='consoles'),
    # path('gaming-accessories/', views.ProductListView.as_view(), name='gaming-accessories'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('return-cancellation/', ReturnCancellationView.as_view(), name='return-cancellation'),
    path('shipping/', ShipplingPolicyView.as_view(), name='shipping'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('term-condition/', TermConditionView.as_view(), name='term-condition'),
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
    # Testing
    path('test/', send_password_reset_email, name='test'),
    #     Password Change Urls
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
]