# Generated by Django 2.0.1 on 2018-12-07 17:23

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20181207_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('deals', 'Deals'), ('news', 'News')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.CharField(choices=[('6', 'Half Yearly'), ('3', 'Quaterly'), ('12', 'Yearly'), ('1', 'Monthly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='plan',
            name='security_deposit',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5, validators=[shop.models.min_value_validator]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='subscription_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5, validators=[shop.models.min_value_validator]),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('N', 'New'), ('U', 'Used')], default='new', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('O', 'Out of Stock'), ('I', 'In Stock')], default='Inactive', max_length=20),
        ),
    ]