# Generated by Django 2.0.1 on 2019-07-04 12:19

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20190626_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='product',
        ),
        migrations.RemoveField(
            model_name='blogattribute',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='blogattribute',
            name='blog',
        ),
        migrations.AlterField(
            model_name='csvimporter',
            name='path',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/sonupal/Documents/hunter/gamehunter/media'), upload_to='csv_file_uploads', validators=[shop.models.validate_csv_file]),
        ),
        migrations.AlterField(
            model_name='plan',
            name='type',
            field=models.CharField(choices=[('GB', 'Game Based'), ('SB', 'Subscription Based')], default='SB', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='developer',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_developer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='developer', to='shop.Brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Genre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('I', 'In Stock'), ('O', 'Out of Stock'), ('S', 'Subscription Only')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_manufacturer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufacturer', to='shop.Brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='plan',
            field=models.ManyToManyField(blank=True, to='shop.Plan'),
        ),
        migrations.AlterField(
            model_name='product',
            name='publisher',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_publisher': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher', to='shop.Brand'),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('coverpage_bottom', 'Coverpage Bottom'), ('coverpage_top', 'Coverpage Top'), ('coverpage_center', 'Coverpage Center'), ('banner_left', 'Banner Left'), ('banner_right', 'Banner Right')], default='coverpage_top', max_length=100),
        ),
        migrations.AlterField(
            model_name='sellyourgames',
            name='game_category',
            field=models.CharField(choices=[('xbox_one', 'Xbox One'), ('ps4', 'Playstation 4')], max_length=30),
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.DeleteModel(
            name='BlogAttribute',
        ),
    ]