# Generated by Django 3.1.5 on 2021-02-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_listing_last_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='final_bid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]