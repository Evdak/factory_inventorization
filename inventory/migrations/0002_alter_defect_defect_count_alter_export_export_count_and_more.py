# Generated by Django 4.0.3 on 2022-04-11 17:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defect',
            name='defect_count',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='export',
            name='export_count',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='import',
            name='import_count',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_count',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество на складе'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='trash_count',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
    ]
