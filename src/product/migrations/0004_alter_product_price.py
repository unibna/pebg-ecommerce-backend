# Generated by Django 3.2.25 on 2024-08-05 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20240804_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
