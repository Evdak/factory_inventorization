# Generated by Django 4.0.3 on 2022-04-20 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_product_product_export_only'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defect',
            options={'verbose_name': 'Брак', 'verbose_name_plural': 'Брак'},
        ),
        migrations.AlterModelOptions(
            name='export',
            options={'verbose_name': 'Отгрузка', 'verbose_name_plural': 'Отгрузки'},
        ),
        migrations.RemoveField(
            model_name='export',
            name='export_price',
        ),
        migrations.RemoveField(
            model_name='import',
            name='import_price',
        ),
        migrations.AddField(
            model_name='trash',
            name='trash_name_str',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True, verbose_name='Наименование изделия'),
        ),
        migrations.AlterField(
            model_name='export',
            name='export_name',
            field=models.ForeignKey(limit_choices_to={'product_export_only': True}, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.product', verbose_name='Наименование изделия'),
        ),
        migrations.AlterField(
            model_name='trash',
            name='trash_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.defect', verbose_name='Наименование изделия'),
        ),
    ]