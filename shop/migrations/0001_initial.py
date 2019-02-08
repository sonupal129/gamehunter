# Generated by Django 2.0.1 on 2018-12-07 14:05

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('attribute', models.CharField(default='', max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Attribute',
            },
        ),
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog_Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, help_text='Will Update Soon', max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Attribute')),
            ],
            options={
                'verbose_name': 'Blog Attribute',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='media/test')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='', max_length=50, unique=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=500)),
            ],
            options={
                'verbose_name': 'Game Genre',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=shop.models.get_product_photo_path)),
                ('item_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['item_order'],
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=200)),
                ('duration', models.CharField(choices=[('yearly', 'Yearly'), ('half-yearly', 'Half Yearly'), ('quaterly', 'Quaterly'), ('monthly', 'Monthly')], default='Monthly', max_length=20)),
                ('description', ckeditor.fields.RichTextField()),
                ('subscription_amount', models.CharField(max_length=10)),
                ('security_deposit', models.CharField(max_length=10)),
                ('term_condition', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/test')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='media/test')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Enter Value of Attribute', max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Attribute')),
            ],
            options={
                'verbose_name': 'Product Attribute',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.BaseModel')),
                ('date_created', models.DateField(auto_created=True)),
                ('title', models.CharField(help_text='Title Name of Blog/Article', max_length=150)),
                ('blog_type', models.CharField(choices=[('deals', 'Deals'), ('news', 'News'), ('blog', 'Blog')], default='blog', max_length=10)),
                ('description', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(default='', max_length=120)),
                ('card_image', models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 370W x 220H', null=True, upload_to='media/test', validators=[shop.models.Blog.validate_card_image])),
                ('cover_image', models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 872W x 472H', null=True, upload_to='media/test', validators=[shop.models.Blog.validate_cover_image])),
            ],
            bases=('shop.basemodel',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.BaseModel')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='', max_length=120, verbose_name='Slug')),
                ('description', ckeditor.fields.RichTextField()),
                ('launch_date', models.DateField()),
                ('item_status', models.CharField(choices=[('O', 'Out of Stock'), ('I', 'In Stock')], default='Inactive', max_length=20)),
                ('condition', models.CharField(choices=[('N', 'New'), ('U', 'Used')], default='new', max_length=10)),
                ('mrp', models.DecimalField(decimal_places=0, default=0, max_digits=5, validators=[shop.models.min_value_validator])),
                ('discount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=2, validators=[shop.models.min_value_validator])),
                ('hunter_discount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=2, validators=[shop.models.min_value_validator])),
                ('total_discount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=2)),
                ('delivery_charges', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=4)),
                ('active', models.BooleanField()),
                ('brand', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Genre')),
                ('plan', models.ManyToManyField(to='shop.Plan')),
            ],
            bases=('shop.basemodel',),
        ),
        migrations.AddField(
            model_name='product_attribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='blog_attribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Blog'),
        ),
        migrations.AddField(
            model_name='blog',
            name='product',
            field=models.ManyToManyField(related_name='blog', to='shop.Product'),
        ),
    ]