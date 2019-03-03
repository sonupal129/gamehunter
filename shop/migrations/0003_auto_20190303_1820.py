# Generated by Django 2.0.1 on 2019-03-03 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20190302_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(blank=True, choices=[('U', 'Used'), ('N', 'New')], default='N', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('I', 'In Stock'), ('S', 'Subscription Only'), ('O', 'Out of Stock')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_bottom', 'Coverpage Bottom'), ('banner_right', 'Banner Right'), ('banner_left', 'Banner Left'), ('coverpage_center', 'Coverpage Center'), ('coverpage_top', 'Coverpage Top')], default='coverpage_top', max_length=100),
        ),
    ]
