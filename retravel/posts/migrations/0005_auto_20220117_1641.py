# Generated by Django 3.2.11 on 2022-01-17 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220117_1638'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='post',
            name='posts_post_slug_59b922_idx',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]