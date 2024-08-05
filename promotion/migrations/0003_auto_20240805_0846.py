# Generated by Django 3.2.25 on 2024-08-05 08:46

from django.db import migrations
import enumfields.fields
import promotion.enums


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_alter_promotion_is_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionresult',
            name='data_type',
            field=enumfields.fields.EnumField(default='STRING', enum=promotion.enums.PromotionResultDataTypeEnum, max_length=32),
        ),
        migrations.AlterField(
            model_name='promotioncondition',
            name='field',
            field=enumfields.fields.EnumField(default='PRODUCT', enum=promotion.enums.PromotionConditionFieldEnum, max_length=10),
        ),
    ]
