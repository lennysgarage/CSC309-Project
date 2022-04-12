# Generated by Django 4.0.2 on 2022-03-16 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0004_alter_blog_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liked_blog', to='blogs.blog')),
                ('likedby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likedby_blog_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='likeblog',
            constraint=models.UniqueConstraint(fields=('blog', 'likedby'), name='unique_blog_likes'),
        ),
    ]
