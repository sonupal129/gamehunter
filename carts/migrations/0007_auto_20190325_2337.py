# Generated by Django 2.0.1 on 2019-03-25 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20190319_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='shipping_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('UO', 'Unverified Order'), ('SP', 'Order Shipped'), ('CO', 'Order Completed'), ('OC', 'Order Confirmed'), ('RTOC', 'RTO Completed'), ('RTO', 'RTO'), ('PR', 'Pickup Requested'), ('IP', 'In Process'), ('OD', 'Order Delivered')], default='UO', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
