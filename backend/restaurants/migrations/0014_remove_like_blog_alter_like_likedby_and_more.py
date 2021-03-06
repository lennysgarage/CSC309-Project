# Generated by Django 4.0.2 on 2022-03-16 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0013_merge_0010_follow_unique_follow_0012_like_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='blog',
        ),
        migrations.AlterField(
            model_name='like',
            name='likedby',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likedby_restaurant_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('restaurant', 'likedby'), name='unique_restaurant_likes'),
        ),
    ]
