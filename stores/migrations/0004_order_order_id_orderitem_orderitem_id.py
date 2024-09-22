# Generated by Django 5.0.7 on 2024-09-22 22:19

import stores.models.order_model
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_orderitem_status_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=stores.models.order_model.get_random_ids, max_length=15),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_id',
            field=models.CharField(default=stores.models.order_model.get_random_ids, max_length=15),
        ),
    ]
