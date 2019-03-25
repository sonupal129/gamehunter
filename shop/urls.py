from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'shop'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    # path('consoles/', views.ProductListView.as_view(), name='consoles'),
    # path('gaming-accessories/', views.ProductListView.as_view(), name='gaming-accessories'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('return-cancellation/', views.ReturnCancellationView.as_view(), name='return-cancellation'),
    path('shipping/', views.ShipplingPolicyView.as_view(), name='shipping'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('term-condition/', views.TermConditionView.as_view(), name='term-condition'),
    path('login/', views.login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.signup_page, name='signup'),
    path('subscription-plans/', views.SubscriptionPlanView.as_view(), name='subscription-list'),
    path('articles/<slug:slug>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('search/', views.product_search, name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<path:slug>/', views.ProductListView.as_view(), name='product-list'),
    path('subscription-plans/<slug:slug>', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('my-orders/', login_required(views.MyOrderView.as_view()), name='orders'),
    path('coming-soon/', views.ComingSoonView.as_view(), name='coming-soon'),
    path('my-account/', views.MyAccountView.as_view(), name='my-account'),
    path('sell-ur-games/', views.SellYourGamesView.as_view(), name='sell-games'),
]
