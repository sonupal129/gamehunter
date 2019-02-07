from django.db import models
from django.contrib.auth.models import User
from shop.models import BaseModel, Address, Product, Plan
import random, datetime
from jsonfield import JSONField
from django.shortcuts import HttpResponseRedirect, redirect
from django.core.exceptions import ObjectDoesNotExist
from carts.signals import new_order_received, new_subscription_order_received
# Create your models here.


class ProductCartManager(models.Manager):

    def create_or_get_cart(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = Cart.objects.filter(cart_id=cart_id)
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
        return cart_obj, new_obj

    def create_cart(self, user=None):
        print(user.is_authenticated)
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(BaseModel):
    cart_id = models.CharField(max_length=17, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='products', blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="plan")
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
            total += self.plan.get_plan_selling_price()
            total += self.plan.get_security_deposit()
        for p in self.products.all():
            total += p.get_mrp_and_selling_price()[0]
        return total

    def get_mrp(self):
        total = 0
        if self.plan:
            total += self.plan.subscription_amount
            total += self.plan.get_security_deposit()
        for p in self.products.all():
            total += p.get_mrp_and_selling_price()[1]
        return total

    def total_cart_items_count(self):
        total_count = self.products.all().count()
        if self.plan:
            total_count += 1
        return total_count

    def total_items_list(self):
        items = []
        if self.plan:
            items.append(self.plan)
            for p in self.products.all():
                items.append(p)
            return items
        else:
            return self.products.all()

    def remove_plan(self):
        if self.plan:
            self.plan = None
            return self.save(update_fields=["plan"])

    def create_product_orders(self, **kwargs):
        order_created = 1
        if self.payment_status == "Credit":
            for product in self.products.all():
                order_id = f"{self.cart_id}_{order_created}"
                print(order_id)
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
                    new_order_received.send(sender=ProductOrders, suborder=order)
                    order_created += 1
                else:
                    print("Object is Available in System Can't Create New")

    def create_subscription_order(self, **kwargs):
        if self.plan and self.payment_status == "Credit":
            order_id = "SUB_" + str(self.cart_id)
            date = datetime.datetime.now()
            data = {"payment_method": "PREPAID", "subscription_amount": self.plan.get_plan_selling_price(),
                    "security_deposit": self.plan.get_security_deposit(), "subscription_duration": self.plan.duration,
                    "extra_month": self.plan.additional_month, "available_swaps": self.plan.swaps, "active": True,
                    "user": self.user, "cart": self, "address": self.address}
            days = (int(data.get("subscription_duration")) + int(data.get("extra_month"))) * 30
            end_date = date + datetime.timedelta(days)
            data["expiry_date"] = end_date
            try:
                subscription = SubscriptionOrders.objects.get(suborder_id=order_id)
            except ObjectDoesNotExist:
                subscription = SubscriptionOrders.objects.create(suborder_id=order_id, **data)
                new_subscription_order_received.send(sender=SubscriptionOrders, suborder=subscription)
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

    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    suborder_id = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, null=True, blank=True, default="UO")
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, blank=True, null=True)
    condition = models.CharField(max_length=10, blank=True, null=True)
    mrp = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    discount = models.CharField(max_length=10, blank=True, null=True)
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


class SubscriptionOrders(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="subscription")
    suborder_id = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(blank=False, default=True)
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    subscription_amount = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    security_deposit = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0)
    subscription_duration = models.DecimalField(default=0, blank=False, max_digits=2, decimal_places=0)
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

