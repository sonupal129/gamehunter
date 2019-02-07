# Generated by Django 2.0.1 on 2019-02-05 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0019_auto_20190204_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorders',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
        migrations.AddField(
            model_name='subscriptionorders',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('SP', 'Order Shipped'), ('CO', 'Order Completed'), ('RTOC', 'RTO Completed'), ('RTO', 'RTO'), ('OD', 'Order Delivered'), ('PR', 'Pickup Requested'), ('OC', 'Order Confirmed'), ('IP', 'In Process'), ('UO', 'Unverified Order')], default='UO', max_length=20, null=True),
        ),
    ]
