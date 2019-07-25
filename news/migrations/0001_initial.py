# Generated by Django 2.0.1 on 2019-07-04 12:19

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0016_auto_20190704_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('title', models.CharField(db_index=True, help_text='Title Name of Blog/Article', max_length=150)),
                ('description', ckeditor.fields.RichTextField()),
                ('status', models.CharField(choices=[('P', 'Published'), ('U', 'Unpublished')], default='U', max_length=15)),
                ('slug', models.SlugField(default='', max_length=120)),
                ('card_image', models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 250W x 250H', null=True, upload_to='other_file_upload_location')),
                ('cover_image', models.ImageField(help_text='For Better Viewing Experience Please make sure Image size should be 872W x 472H', null=True, upload_to='other_file_upload_location')),
                ('author', models.ForeignKey(blank=True, default='Admin', on_delete=django.db.models.deletion.SET_DEFAULT, to='news.Author')),
            ],
        ),
        migrations.CreateModel(
            name='NewsAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, help_text='Please enter desired value', max_length=200)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Attribute')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.News')),
            ],
            options={
                'verbose_name_plural': 'News Attribute',
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('category_title_meta', models.CharField(blank=True, max_length=50, null=True)),
                ('category_description_meta', models.CharField(blank=True, max_length=100, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='news.NewsCategory')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.NewsCategory'),
        ),
    ]