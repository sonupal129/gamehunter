# Generated by Django 2.0.1 on 2019-02-08 19:02

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0046_auto_20190205_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('news', 'News'), ('deals', 'Deals')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='blog',
            name='card_image',
            field=models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 370W x 220H', null=True, upload_to=shop.models.other_file_upload_location, validators=[shop.models.Blog.validate_card_image]),
        ),
        migrations.AlterField(
            model_name='blog',
            name='cover_image',
            field=models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 872W x 472H', null=True, upload_to=shop.models.other_file_upload_location, validators=[shop.models.Blog.validate_cover_image]),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.other_file_upload_location),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='csvimporter',
            name='path',
            field=models.FileField(upload_to=shop.models.other_file_upload_location, validators=[shop.models.validate_csv_file]),
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to=shop.models.get_product_photo_path, validators=[shop.models.validate_image_file]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.other_file_upload_location),
        ),
        migrations.AlterField(
            model_name='plan',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.other_file_upload_location),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('O', 'Out of Stock'), ('I', 'In Stock')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_center', 'Coverpage Center'), ('coverpage_bottom', 'Coverpage Bottom'), ('coverpage_top', 'Coverpage Top'), ('banner_left', 'Banner Left'), ('banner_right', 'Banner Right')], default='coverpage_top', max_length=100),
        ),
    ]
