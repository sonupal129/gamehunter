from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from shop.models import Attribute, UserProfile
from ckeditor.fields import RichTextField
# Create your models here.

class NewsCategory(MPTTModel):
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


class Author(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True, null=True)


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    category = models.ForeignKey(NewsCategory,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150, help_text='Title Name of Blog/Article', db_index=True)
    description = RichTextField(config_name='default')
    status = models.CharField(choices={("P", "Published"), ("U", "Unpublished")}, max_length=15, default="U")
    date_created = models.DateField(auto_created=True)
    slug = models.SlugField(blank=False, default='', max_length=120, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, blank=True, default="Admin")

    class Meta:
        verbose_name_plural = "News"

    def validate_card_image(self):
        limit = 370 * 220
        if self.size > limit:
            raise ValidationError(f"Uploaded Image W*H Should be {limit} in size")

    def validate_cover_image(self):
        limit = 872 * 472
        if self.size > limit:
            raise ValidationError(f"Uploaded Image W*H Should be {limit} in size")

    card_image = models.ImageField(
        help_text='For Better Viewing Experience Please make sure Image size should be 250W x 250H',
        upload_to="other_file_upload_location", blank=False, null=True)
    cover_image = models.ImageField(upload_to="other_file_upload_location", blank=False, null=True,
                                    help_text='For Better Viewing Experience Please make sure Image size should be 872W x 472H')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:article-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Blog, self).save(*args, **kwargs)

class NewsAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, db_index=True)
    value = models.CharField(max_length=200, help_text='Please enter desired value', blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = "News Attribute"