from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
import datetime, os
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User
from uuid import uuid4
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.html import mark_safe, html_safe, force_text, format_html, escape
import bleach
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


def validate_csv_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.csv']
    if not ext.lower() in valid_extension:
        raise ValidationError("Unsupported file extension type, Please use .csv format file only")


def validate_image_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.jpg', '.jpeg']
    if not ext.lower() in valid_extension:
        raise ValidationError("Unsupported file extension type, Please use JPG files only")


def min_value_validator(value):
    if value < 0:
        raise ValidationError("Value can't be less than 0")
    pass


def get_product_photo_path(instance, filename):
    if instance.product:
        filename = str(uuid4()) + '.jpg'
        return os.path.join("uploads/products/%d" % instance.product.id, filename)
    if instance.promocard:
        return os.path.join("uploads/promocards/%d" % instance.promocard.id, filename)


def other_file_upload_location(instance, filename):
    if isinstance(instance, Brand):
        filename = str(uuid4()) + '.jpg'
        return os.path.join("uploads/brands/", filename)
    elif isinstance(instance, Plan):
        filename = str(uuid4()) + '.jpg'
        return os.path.join("uploads/plans/", filename)
    elif isinstance(instance, Blog):
        filename = str(uuid4()) + '.jpg'
        return os.path.join("uploads/blogs/", filename)
    else:
        pass


class Category(MPTTModel):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, unique=True, default='')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    slug = models.SlugField(db_index=True, null=True, blank=True)
    category_title_meta = models.CharField(max_length=50, null=True, blank=True)
    category_description_meta = models.CharField(max_length=100, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product-list", kwargs={"slug": self.slug}) 

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        if not self.is_root_node():
            slug_list = [slugify(ancestor.name) for ancestor in self.get_ancestors(include_self=True)]
            print(slug_list)
            self.slug = '/'.join(slug_list)
        else:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def get_parent_with_self(self):
        return self.get_ancestors(include_self=True)

class Attribute(MPTTModel):
    name = models.CharField(max_length=50, unique=True, default='')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Brand(models.Model):
    name = models.CharField(db_index=True, max_length=50, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to=other_file_upload_location, blank=True, null=True,
                              validators=[validate_image_file])
    is_developer = models.BooleanField('Developer', blank=True, default=True)
    is_publisher = models.BooleanField('Publisher', blank=True, default=True)
    is_manufacturer = models.BooleanField('Manufacturer', blank=True, default=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    genre = models.CharField(db_index=True, max_length=20, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)

    class Meta:
        verbose_name = "Game Genre"

    def __str__(self):
        return self.genre


class Plan(models.Model):
    type_choices = {
        ("SB", "Subscription Based"),
        ("GB", "Game Based"),
    }
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=type_choices, default="SB")
    duration = models.PositiveSmallIntegerField(default=0)
    additional_month = models.PositiveSmallIntegerField(default=0)
    swaps = models.PositiveSmallIntegerField('Available Swaps', default=0)
    description = RichTextField(config_name='default')
    subscription_amount = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0,
                                              validators=[min_value_validator])
    security_deposit = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0,
                                           validators=[min_value_validator])
    refundable = models.BooleanField(blank=True, default=True)
    term_condition = RichTextField(config_name='default')
    image = models.ImageField(upload_to=other_file_upload_location, blank=True, null=True, validators=[validate_image_file])
    image1 = models.ImageField(upload_to=other_file_upload_location, blank=True, null=True, validators=[validate_image_file])
    slug = models.SlugField('Slug', max_length=120, blank=False, default="", db_index=True)
    discount = models.DecimalField(default=0, blank=True, max_digits=2, decimal_places=0,
                                   validators=[min_value_validator])
    active = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Plan, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:subscription-detail", kwargs={'slug': self.slug})

    def get_plan_selling_price(self):
        if self.type == "SB" and self.discount != 0:
            final_selling_price = self.subscription_amount - (self.subscription_amount * self.discount // 100)
            return final_selling_price
        else:
            return self.subscription_amount

    def get_monthly_subscription_selling_price(self, cached=True):
        cache_key = '_'.join([self.get_absolute_url(), "monthly_subscription_price"])
        cached_value = cache.get(cache_key)
        if cached and cached_value:
            return cached_value
        if self.type == "SB":
            monthly_selling_price = self.get_plan_selling_price() // self.duration
            cache.set(cache_key, monthly_selling_price)
            return monthly_selling_price
        return ""

    def get_monthly_subscription_mrp(self, cached=True):
        cache_key = '_'.join([self.get_absolute_url(), "monthly_subscription_mrp"])
        cached_value = cache.get(cache_key)
        if cached_value and cached:
            return cached_value
        else:
            monthly_selling_mrp = self.subscription_amount // self.duration
            cache.set(cache_key, monthly_selling_mrp)
            return monthly_selling_mrp

    def is_object_of_plan_class(self):
        if isinstance(self, Plan):
            return True
        else:
            return False

    def get_security_deposit(self):
        return self.security_deposit

    def get_plan_total_duration(self):
        if self.type == "SB":
            total_months = self.duration + self.additional_month
            return total_months
        else:
            if self.duration >= 99:
                return "Lifetime!"
            return self.duration

    def available_swaps(self):
        if self.type == "SB":
            return self.swaps//self.duration
        return self.swaps

    def get_plan_description(self):
        if len(self.description) > 300:
            description = self.description[:270] + '...'
            return description.strip()
        return self.description.strip()


class PromoCard(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    card_type = {('coverpage_top', 'Coverpage Top'),
                 ('coverpage_center', 'Coverpage Center'),
                 ('coverpage_bottom', 'Coverpage Bottom'),
                 ('banner_left', 'Banner Left'),
                 ('banner_right', 'Banner Right'), }

    name = models.CharField(max_length=70, blank=True,)
    description = models.CharField(max_length=120, blank=True, null=True)
    promocard_type = models.CharField(choices=card_type, max_length=100, default='coverpage_top')
    active = models.BooleanField(blank=True)
    link = models.CharField(max_length=200, null=True, default='', blank=True)

    def __str__(self):
        return self.name

    def get_promo_image(self):
        if not hasattr(self, '__default_photo'):
            self.__default_photo = self.photo_set.first()
        return self.__default_photo


class Product(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    plan = models.ManyToManyField(Plan, blank=True)
    slug = models.SlugField('Slug', max_length=120, blank=False, default='', db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = RichTextField(config_name='default', blank=True)
    launch_date = models.DateField(blank=True, null=True, db_index=True)
    item_status = models.CharField(choices={('I', 'In Stock'), ('O', 'Out of Stock'), ('S', 'Subscription Only'),},
                                   max_length=20, default='O')
    developer = models.ForeignKey(Brand, limit_choices_to={'is_developer': True}, null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='developer')
    publisher = models.ForeignKey(Brand, limit_choices_to={'is_publisher': True}, null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='publisher')
    manufacturer = models.ForeignKey(Brand, limit_choices_to={'is_manufacturer': True}, null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='manufacturer')
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=10, choices={('U', 'Used'), ('N', 'New')}, default='N', null=True, blank=True)
    mrp = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=0,
                              validators=[min_value_validator])
    discount = models.DecimalField(default=0, blank=True, max_digits=2, decimal_places=0,
                                   validators=[min_value_validator])
    hunter_discount = models.DecimalField(default=0, blank=True, max_digits=2, decimal_places=0,
                                          validators=[min_value_validator])
    total_discount = models.DecimalField(default=0, blank=True, max_digits=2, decimal_places=0)
    delivery_charges = models.DecimalField(default=0, blank=True, max_digits=4, decimal_places=0)
    active = models.BooleanField(blank=True)
    is_featured = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.total_discount = self.discount + self.hunter_discount
        if self.total_discount > 99:
            self.total_discount = self.discount

        if not self.publisher:
            self.slug = slugify(self.name + '-for-' + self.category.name)
        else:
            self.slug = slugify(self.name + '-by-' + self.publisher.name + '-for-' + self.category.name)
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Family."""
        return reverse("shop:product-detail", kwargs={'slug': self.slug})

    def get_product_attribute(self, attribute_name: str):
        try:
            return self.productattribute.get(attribute__name=attribute_name)
        except ObjectDoesNotExist:
            return "" 

    def get_pay_per_game_subscription_price(self, cached=True):
        cache_key = '_'.join([self.get_absolute_url(), "pay_per_game_subscription_price"])
        cached_value = cache.get(cache_key)
        if cached_value and cached:
            return cached_value
        price = self.get_product_attribute(attribute_name="game_based_plan_price")
        cache.set(cache_key, price)
        return price

    def get_old_slug(self):
        return self.get_product_attribute("old_slug")

    def add_to_trending_products(self):
        attr = self.get_product_attribute("trending")
        if attr:
            attr.value = int(attr.value) + 1
            attr.save()
        else:
            ProductAttribute.objects.create(product=self, attribute=Attribute.objects.get(name="trending"), value=1)

    def get_default_photo(self):
        if not hasattr(self, '__default_photo'):
            self.__default_photo = self.photo_set.all().order_by("id").first()
        return self.__default_photo

    def get_mrp_and_selling_price(self):
        selling_price = self.mrp - (self.mrp * self.total_discount // 100) + self.delivery_charges
        mrp = (selling_price * 100) // (100 - self.total_discount)
        return selling_price, mrp

    def game_trailer(self, cached=True):
        cache_key = '_'.join([self.get_absolute_url(), "game_trailer"])
        cached_value = cache.get(cache_key)
        if cached and cached_value:
            return cached_value
        trailer = self.get_product_attribute("game_trailer")
        if trailer:
            cache.set(cache_key, trailer.value)
            return trailer.value
        else:
            return None

    def photos_in_ascendant(self):
        if self.photo_set.all():
            return self.photo_set.all().order_by("id")


class ProductAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, db_index=True)
    value = models.CharField(max_length=200, help_text='Enter Value of Attribute', blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True,
                                related_name="productattribute")

    def __str__(self):
        return str(self.attribute) + "-" + str(self.product)

    class Meta:
        verbose_name = "Product Attribute"


class Photo(models.Model):
    file = models.ImageField(upload_to=get_product_photo_path, null=False, blank=False, validators=[validate_image_file])
    item_order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    promocard = models.ForeignKey(PromoCard, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["item_order"]

class UserProfile(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(null=True, blank=True)
    subscribed = models.BooleanField(blank=True)

    def __str__(self):
        return self.user.email

    def has_subscription(self):
        try:
            self.user.subscription.filter(active=True).first()
            return True
        except ObjectDoesNotExist:
            return False

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance, subscribed=True)
        instance.userprofile.save()


class AddressManager(models.Manager):

    def get_or_create_address(self, user):
        userprofile = user.userprofile
        address_obj = Address.objects.filter(user=userprofile)
        if address_obj:
            return address_obj.first()
        else:
            address_obj = Address.objects.create(user=userprofile)
            return address_obj


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)

    objects = AddressManager()

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address


class CSVImporter(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_type = models.CharField("Data Type", choices=(("PD", "Product"),), max_length=10)
    path = models.FileField(upload_to='csv_file_uploads', storage=FileSystemStorage(location=settings.MEDIA_ROOT),
                            blank=False, null=False, validators=[validate_csv_file])

    class Meta:
        verbose_name_plural = "CSV Importer"

    def __str__(self):
        return str(self.path)


class ExceptionLog(models.Model):
    """ Model for catching exception when debug is False """

    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    views = models.CharField("View", max_length=60)
    exceptionclass = models.CharField("Exception Class", max_length=120)
    message = models.TextField("Exception Message", max_length=1000)


class SellYourGames(models.Model):
    game_choice = {("xbox_one", "Xbox One"),
                   ("ps4", "Playstation 4")
                   }

    game_name = models.CharField(max_length=150, blank=True, null=True)
    game_category = models.CharField(max_length=30, choices=game_choice)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)