# Generated by Django 3.2.11 on 2022-01-17 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]