# Generated by Django 5.0.7 on 2024-09-22 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_rename_quantity_product_available_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
