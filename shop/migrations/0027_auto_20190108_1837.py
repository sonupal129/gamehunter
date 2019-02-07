# Generated by Django 2.0.1 on 2019-01-08 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_auto_20190108_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('U', 'Used'), ('N', 'New')], default='N', max_length=10),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_center', 'Coverpage Center'), ('banner_left', 'Banner Left'), ('banner_right', 'Banner Right'), ('coverpage_bottom', 'Coverpage Bottom'), ('coverpage_top', 'Coverpage Top')], default='coverpage_top', max_length=100),
        ),
    ]
