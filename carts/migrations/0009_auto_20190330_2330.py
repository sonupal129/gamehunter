# Generated by Django 2.0.1 on 2019-03-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_auto_20190329_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionorders',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('OC', 'Order Confirmed'), ('RTOC', 'RTO Completed'), ('OD', 'Order Delivered'), ('CO', 'Order Completed'), ('PR', 'Pickup Requested'), ('RTO', 'RTO'), ('UO', 'Unverified Order'), ('IP', 'In Process'), ('SP', 'Order Shipped')], default='UO', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptionorders',
            name='subscription_duration',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]