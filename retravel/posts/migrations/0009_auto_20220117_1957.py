# Generated by Django 3.2.11 on 2022-01-17 10:57

from django.conf import settings
from django.db import migrations, models
import posts.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_remove_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=posts.storage.OverwriteStorage(), upload_to='post_imgs'),
        ),
        migrations.AlterField(
            model_name='post',
            name='like_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]