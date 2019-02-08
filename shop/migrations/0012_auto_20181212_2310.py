# Generated by Django 2.0.1 on 2018-12-12 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20181212_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='promo_card',
            new_name='promocard',
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(choices=[('blog', 'Blog'), ('news', 'News'), ('deals', 'Deals')], default='blog', max_length=10),
        ),
        migrations.AlterField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.CharField(choices=[('3', 'Quaterly'), ('1', 'Monthly'), ('12', 'Yearly'), ('6', 'Half Yearly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('I', 'In Stock'), ('O', 'Out of Stock')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='link',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_bottom', 'Coverpage Bottom'), ('banner_left', 'Banner Left'), ('coverpage_top', 'Coverpage Top'), ('coverpage_center', 'Coverpage Center'), ('banner_right', 'Banner Right')], default='Coverpage Top', max_length=100),
        ),
    ]