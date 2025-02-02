from django.db import models
from django.contrib.auth.models import User
from shop.models import Address, Product, Plan
import random, datetime
from jsonfield import JSONField
from django.shortcuts import HttpResponseRedirect, redirect
from django.core.exceptions import ObjectDoesNotExist
from carts.slacknotification import new_product_order_received, new_subscription_order_received
from background_task import background
# Create your models here.


class ProductCartManager(models.Manager):

    def create_or_get_cart(self, request):
        qs = Cart.objects.filter(cart_id=request.session.get("cart_id", None))
        if qs.count() == 1:
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create_cart(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.cart_id
        return cart_obj

    def create_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    cart_id = models.CharField(db_index=True, max_length=20, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='products', blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="plan")
    pay_game_products = models.ManyToManyField(Product, related_name='pay_game_products', blank=True)
    total_mrp = models.DecimalField(default=0, blank=True, max_digits=5, decimal_places=0)
    total_selling_price = models.DecimalField(default=0, blank=True, max_digits=5, decimal_places=0)
    total_discount = models.DecimalField(default=0, blank=True, max_digits=5, decimal_places=0)
    updated = models.DateTimeField("Recently Updated", auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    payment_request = JSONField(blank=True, null=True)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=10, blank=True, null=True)

    objects = ProductCartManager()

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name_plural = "Carts"

    def save(self, *args, **kwargs):
        if not self.cart_id:
            id = "GHPDO" + str(random.randrange(111111111111, 999999999999))
            while Cart.objects.filter(cart_id=id):
                id = "GHPDO" + str(random.randrange(111111111111, 999999999999))
            self.cart_id = id
        super(Cart, self).save(*args, **kwargs)

    def get_discount(self):
        discount_price = self.total_mrp - self.total_selling_price
        self.total_discount = discount_price
        self.save()
        return discount_price

    def get_selling_price(self):
        total = 0
        if self.plan:
            total += self.plan.get_plan_selling_price() + self.plan.get_security_deposit()
        total += sum(p.get_mrp_and_selling_price()[0] for p in self.products.all())
        total += sum(int(p.get_pay_per_game_subscription_price().value) for p in self.pay_game_products.all())
        return int(total)

    def get_mrp(self):
        total = 0
        if self.plan:
            total += self.plan.subscription_amount + self.plan.get_security_deposit()
        total += sum(p.get_mrp_and_selling_price()[1] for p in self.products.all())
        total += sum(int(p.get_pay_per_game_subscription_price().value) for p in self.pay_game_products.all())
        return int(total)

    def total_cart_items_count(self):
        total_count = self.products.all().count() + self.pay_game_products.all().count()
        if self.plan:
            total_count += 1
        return total_count

    def total_items_list(self):
        products = []
        pay_per_game_products = []
        for p in self.products.all():
            if p.item_status == "O" or not p.active:
                self.products.remove(p)
            else:
                products.append(p)
        for p in self.pay_game_products.all():
            if p.item_status == "O" or not p.active:
                self.pay_game_products.remove(p)
            else:
                pay_per_game_products.append(p)
        if self.plan is not None:
            if self.plan.active:
                products.append(self.plan)
            else:
                self.plan = None
                self.save(update_fields=["plan"])
        return products, pay_per_game_products

    def remove_plan(self):
        if self.plan:
            self.plan = None
            return self.save(update_fields=["plan"])

    def create_product_orders(self, **kwargs):
        order_created = 1
        if self.payment_status == "Credit":
            for product in self.products.all():
                order_id = f"{self.cart_id}_{order_created}"
                try:
                    order = ProductOrders.objects.get(suborder_id=order_id)
                except ObjectDoesNotExist:
                    selling_price, mrp = product.get_mrp_and_selling_price()
                    data = {"mrp": mrp, "selling_price": selling_price, "cart": self,
                            "hunter_discount": product.hunter_discount, "total_discount": product.total_discount,
                            "delivery_charges": product.delivery_charges, "address": self.address,
                            "final_selling_price": product.delivery_charges + selling_price,
                            "product": product}
                    if self.payment_status == "Credit":
                        data["payment_method"] = "PREPAID"
                    elif self.payment_status == "COD":
                        data["payment_method"] = "COD"
                    else:
                        data["payment_method"] = "NO METHOD DEFINE"
                    if product.condition == "N":
                        data["condition"] = "NEW"
                    else:
                        data["condition"] = "USED"
                    order = ProductOrders.objects.create(suborder_id=order_id, **data)
                    new_product_order_received(order)
                    order_created += 1
                else:
                    print("Object is Available in System Can't Create New")

    def create_pay_per_game_product_order(self):
        order_created = 1
        if self.payment_status == "Credit":
            for product in self.pay_game_products.all():
                order_id = f"{self.cart_id}_PGP_{order_created}"
                try:
                    order = ProductOrders.objects.get(suborder_id=order_id)
                except ObjectDoesNotExist:
                    data = {"mrp": 0, "selling_price": product.get_pay_per_game_subscription_price(), "cart": self,
                            "hunter_discount": 0, "total_discount": 0,
                            "delivery_charges": 0, "address": self.address,
                            "final_selling_price": product.get_pay_per_game_subscription_price(),
                            "product": product}

                    if self.payment_status == "Credit":
                        data["payment_method"] = "PREPAID"
                    elif self.payment_status == "COD":
                        data["payment_method"] = "COD"
                    else:
                        data["payment_method"] = "NO METHOD DEFINE"
                    data["condition"] = "USED"
                    order = ProductOrders.objects.create(suborder_id=order_id, **data)
                    new_product_order_received(order)
                    order_created += 1
                else:
                    print("Object is Available in System Can't Create New")

    def create_subscription_order(self, **kwargs):
        print(self)
        if self.plan and self.payment_status == "Credit":
            order_id = "SUB_" + str(self.cart_id)
            date = datetime.datetime.now()
            data = {"payment_method": "PREPAID", "subscription_amount": self.plan.get_plan_selling_price(),
                    "security_deposit": self.plan.get_security_deposit(), "subscription_duration": self.plan.duration,
                    "extra_month": self.plan.additional_month, "available_swaps": self.plan.swaps, "active": True,
                    "user": self.user, "cart": self, "address": self.address, "type": self.plan.type}
            days = (int(data.get("subscription_duration")) + int(data.get("extra_month"))) * 30
            end_date = date + datetime.timedelta(days)
            data["expiry_date"] = end_date
            try:
                subscription = SubscriptionOrders.objects.get(suborder_id=order_id)
            except ObjectDoesNotExist:
                subscription = SubscriptionOrders.objects.create(suborder_id=order_id, **data)
                new_subscription_order_received(subscription)
            else:
                print("Subscription is Already Available Can't Create New")


class ProductOrders(models.Model):
    status_choices = {
        ("UO", "Unverified Order"),
        ("OC", "Order Confirmed"),
        ("IP", "In Process"),
        ("PR", "Pickup Requested"),
        ("SP", "Order Shipped"),
        ("RTO", "RTO"),
        ("RTOC", "RTO Completed"),
        ("OD", "Order Delivered"),
        ("CO", "Order Completed"),
    }

    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE, related_name="orders")
    suborder_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, null=True, blank=True, default="UO")
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    shipping_link = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=10, blank=True, null=True)
    mrp = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    tracking_id = models.CharField(max_length=30, blank=True, null=True)
    hunter_discount = models.CharField(max_length=10, blank=True, null=True)
    total_discount = models.CharField(max_length=10, blank=True, null=True)
    selling_price = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    delivery_charges = models.CharField(max_length=10, blank=True, null=True)
    final_selling_price = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.suborder_id

    class Meta:
        verbose_name_plural = "Product Orders"

    def order_tracking_url(self):
        if self.status == "SP" and self.shipping_link:
            return self.shipping_link

    def get_cart(self):
        return self.cart

class SubscriptionOrders(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(null=True, blank=True, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="subscription")
    suborder_id = models.CharField(max_length=25, null=True, blank=True)
    active = models.BooleanField(blank=False, default=True)
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    subscription_amount = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    security_deposit = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    subscription_duration = models.DecimalField(default=0, blank=False, max_digits=3, decimal_places=0)
    extra_month = models.DecimalField(default=0, blank=False, max_digits=2, decimal_places=0)
    available_swaps = models.DecimalField(default=0, blank=False, max_digits=2, decimal_places=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.suborder_id

    class Meta:
        verbose_name_plural = "Subscription Orders"

    def get_subscription_duration(self):
        total_duration = self.subscription_duration + self.extra_month
        return total_duration

