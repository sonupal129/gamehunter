# Generated by Django 2.0.1 on 2019-03-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_auto_20190312_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('RTOC', 'RTO Completed'), ('CO', 'Order Completed'), ('OC', 'Order Confirmed'), ('UO', 'Unverified Order'), ('SP', 'Order Shipped'), ('IP', 'In Process'), ('RTO', 'RTO'), ('PR', 'Pickup Requested'), ('OD', 'Order Delivered')], default='UO', max_length=20, null=True),
        ),
    ]
