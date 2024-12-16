# Generated by Django 5.1.2 on 2024-11-29 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Placed', 'Order Placed'), ('Pending', 'Pending'), ('shipped', 'shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Order Placed', max_length=20, null=True),
        ),
    ]
