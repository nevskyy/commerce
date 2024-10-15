# Generated by Django 4.2.16 on 2024-10-12 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_creating_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.bid'),
        ),
    ]
