# Generated by Django 4.0.3 on 2022-04-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_export_only',
            field=models.BooleanField(default=False, verbose_name='Доступен для ухода'),
        ),
    ]
