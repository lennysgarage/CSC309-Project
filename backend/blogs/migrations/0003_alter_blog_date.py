# Generated by Django 4.0.2 on 2022-03-15 20:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_blog_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, editable=False),
        ),
    ]