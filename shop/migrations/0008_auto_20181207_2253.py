# Generated by Django 2.0.1 on 2018-12-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20181207_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('news', 'News'), ('deals', 'Deals')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.CharField(choices=[('12', 'Yearly'), ('1', 'Monthly'), ('6', 'Half Yearly'), ('3', 'Quaterly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('U', 'Used'), ('N', 'New')], default='new', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('I', 'In Stock'), ('O', 'Out of Stock')], default='Inactive', max_length=20),
        ),
    ]