# Generated by Django 4.0.1 on 2022-02-04 10:27

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='instaAccounts',
            fields=[
                ('username', models.CharField(max_length=30)),
                ('userId', models.CharField(default=accounts.models.idgen, max_length=20, primary_key=True, serialize=False)),
                ('followers', models.JSONField(default=dict)),
                ('following', models.JSONField(default=dict)),
                ('media', models.JSONField(default=dict)),
                ('isVerified', models.BooleanField(default=False)),
                ('isBusiness', models.BooleanField(default=False)),
                ('businessCategory', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('category', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('dailyTrending', models.JSONField(default=dict)),
            ],
        ),
    ]
