# Generated by Django 2.0.1 on 2019-03-15 11:49

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190312_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('U', 'Unpublished'), ('P', 'Published')], default='U', max_length=15),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('deals', 'Deals'), ('news', 'News')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='blog',
            name='card_image',
            field=models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 250W x 250H', null=True, upload_to=shop.models.other_file_upload_location, validators=[shop.models.Blog.validate_card_image]),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('U', 'Used')], default='N', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_center', 'Coverpage Center'), ('coverpage_top', 'Coverpage Top'), ('banner_left', 'Banner Left'), ('coverpage_bottom', 'Coverpage Bottom'), ('banner_right', 'Banner Right')], default='coverpage_top', max_length=100),
        ),
    ]
