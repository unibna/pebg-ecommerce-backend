# Generated by Django 3.2.25 on 2024-08-05 07:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
        ('order', '0002_auto_20240805_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPromotion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_applied', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_promotions', to='order.order')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promotion.promotion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
