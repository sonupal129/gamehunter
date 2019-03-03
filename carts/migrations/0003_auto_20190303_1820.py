# Generated by Django 2.0.1 on 2019-03-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20190302_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorders',
            name='status',
            field=models.CharField(blank=True, choices=[('RTOC', 'RTO Completed'), ('UO', 'Unverified Order'), ('IP', 'In Process'), ('OC', 'Order Confirmed'), ('OD', 'Order Delivered'), ('SP', 'Order Shipped'), ('CO', 'Order Completed'), ('RTO', 'RTO'), ('PR', 'Pickup Requested')], default='UO', max_length=20, null=True),
        ),
    ]
