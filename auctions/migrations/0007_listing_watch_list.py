# Generated by Django 5.1.1 on 2024-09-23 08:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watch_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
