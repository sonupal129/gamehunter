# Generated by Django 2.0.1 on 2019-07-27 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name_plural': 'News'},
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('U', 'Unpublished'), ('P', 'Published')], default='U', max_length=15),
        ),
    ]
