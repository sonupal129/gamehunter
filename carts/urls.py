from django.contrib import admin
from django.urls import path
from . import views, instamojo, emails, slacknotification
from django.contrib.auth.decorators import login_required



app_name = 'carts'

urlpatterns = [
    path('', login_required(views.cart_home), name='cart'),
    path('add/<slug:slug>', views.cart_add_product, name='add'),
    path('add-pay-per-game/<slug:slug>', views.add_pay_per_game_product, name='pay-per-game-product'),
    path('remove/<slug:slug>', views.cart_remove_product, name='remove'),
    path('delete', views.remove_whole_cart, name='delete-all'),
    path('checkout/', views.cart_checkout, name='checkout'),
    path('payment/', instamojo.send_payment_request, name='payment'),
    path('payment/successful', instamojo.redirect_payment_complete, name='payment-successful'),
    path('add/plan/<slug:slug>', views.cart_add_plan, name='add-plan'),
    path('remove/plan/<slug:slug>', views.cart_remove_plan, name='remove-plan'),
    path('test/', views.TestView.as_view(), name='test'),
]
