# Generated by Django 3.1.5 on 2021-02-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]