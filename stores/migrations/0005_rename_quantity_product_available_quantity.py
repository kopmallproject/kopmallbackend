# Generated by Django 5.0.7 on 2024-09-22 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_order_order_id_orderitem_orderitem_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='available_quantity',
        ),
    ]
