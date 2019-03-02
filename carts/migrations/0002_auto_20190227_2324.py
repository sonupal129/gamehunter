# Generated by Django 2.0.1 on 2019-02-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('UO', 'Unverified Order'), ('OD', 'Order Delivered'), ('OC', 'Order Confirmed'), ('SP', 'Order Shipped'), ('IP', 'In Process'), ('RTO', 'RTO'), ('PR', 'Pickup Requested'), ('RTOC', 'RTO Completed'), ('CO', 'Order Completed')], default='UO', max_length=20, null=True),
        ),
    ]
