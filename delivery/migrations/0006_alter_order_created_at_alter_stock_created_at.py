# Generated by Django 5.1.1 on 2024-09-29 14:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_remove_stock_image_alter_order_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 29, 19, 22, 26, 782836), null=True, verbose_name='Buyurtma berilgan vaqt'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Aktsiya yaratilgan vaqt'),
        ),
    ]
