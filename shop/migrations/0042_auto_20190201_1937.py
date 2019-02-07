# Generated by Django 2.0.1 on 2019-02-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0041_auto_20190201_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('deals', 'Deals'), ('blog', 'Blog'), ('news', 'News')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_bottom', 'Coverpage Bottom'), ('coverpage_top', 'Coverpage Top'), ('coverpage_center', 'Coverpage Center'), ('banner_right', 'Banner Right'), ('banner_left', 'Banner Left')], default='coverpage_top', max_length=100),
        ),
    ]
