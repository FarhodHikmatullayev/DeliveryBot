# Generated by Django 5.1.1 on 2024-09-30 05:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_alter_order_created_at_alter_stock_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 30, 10, 29, 31, 599430), null=True, verbose_name='Buyurtma berilgan vaqt'),
        ),
    ]
