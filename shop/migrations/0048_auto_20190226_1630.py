# Generated by Django 2.0.1 on 2019-02-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0047_auto_20190209_0032'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog_Attribute',
            new_name='BlogAttribute',
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('U', 'Used'), ('N', 'New')], default='N', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='item_status',
            field=models.CharField(choices=[('I', 'In Stock'), ('O', 'Out of Stock')], default='O', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='launch_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promocard',
            name='type',
            field=models.CharField(choices=[('banner_right', 'Banner Right'), ('coverpage_bottom', 'Coverpage Bottom'), ('coverpage_center', 'Coverpage Center'), ('coverpage_top', 'Coverpage Top'), ('banner_left', 'Banner Left')], default='coverpage_top', max_length=100),
        ),
    ]
