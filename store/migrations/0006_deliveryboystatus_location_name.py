# Generated by Django 5.1.2 on 2024-11-20 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_deliveryboystatus_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboystatus',
            name='location_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
