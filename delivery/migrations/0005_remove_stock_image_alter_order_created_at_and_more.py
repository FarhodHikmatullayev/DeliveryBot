# Generated by Django 5.1.1 on 2024-09-29 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_stock_image_id_alter_order_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='image',
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 29, 18, 29, 18, 501903), null=True, verbose_name='Buyurtma berilgan vaqt'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 29, 18, 29, 18, 501903), null=True, verbose_name='Aktsiya yaratilgan vaqt'),
        ),
    ]
