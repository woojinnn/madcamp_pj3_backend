# Generated by Django 3.2.11 on 2022-01-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]