# Generated by Django 4.0.1 on 2022-02-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_instaaccounts_comments_instaaccounts_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='comments',
            field=models.IntegerField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='media',
            name='likes',
            field=models.IntegerField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='media',
            name='views',
            field=models.IntegerField(default='', max_length=20),
        ),
    ]
