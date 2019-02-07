# Generated by Django 2.0.1 on 2018-12-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20181212_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.CharField(choices=[('3', 'Quaterly'), ('12', 'Yearly'), ('6', 'Half Yearly'), ('1', 'Monthly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('O', 'Out of Stock'), ('I', 'In Stock')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('banner_left', 'Banner Left'), ('banner_right', 'Banner Right'), ('coverpage_top', 'Coverpage Top'), ('coverpage_center', 'Coverpage Center'), ('coverpage_bottom', 'Coverpage Bottom')], default='Coverpage Top', max_length=100),
        ),
    ]
