# Generated by Django 4.0.2 on 2022-04-18 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0015_remove_restaurant_liked_by'),
        ('blogs', '0005_likeblog_likeblog_unique_blog_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_restaurant', to='restaurants.restaurant'),
        ),
    ]
