from enumfields import EnumField
from django.db import models

from .enums import (
    PromotionTypeEnum,
    PromotionResultDataTypeEnum,
    PromotionConditionFieldEnum,
    PromotionConditionFieldDataTypeEnum,
    PromotionOperatorEnum,
    PromotionGroupOperatorEnum,
)
from base.models import BaseModel


class Promotion(BaseModel):
    name = models.CharField(max_length=512)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PromotionConditionGroup(BaseModel):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='condition_groups'
    )
    operator = EnumField(
        PromotionGroupOperatorEnum,
        default=PromotionGroupOperatorEnum.AND,
        max_length=32,
    )
    
    def __str__(self) -> str:
        return f"{self.operator}"


class PromotionCondition(BaseModel):
    group = models.ForeignKey(
        PromotionConditionGroup,
        on_delete=models.CASCADE,
        related_name='conditions'
    )
    field = EnumField(
        PromotionConditionFieldEnum,
        default=PromotionConditionFieldEnum.PRODUCT
    )
    data_type = EnumField(
        PromotionConditionFieldDataTypeEnum,
        default=PromotionConditionFieldDataTypeEnum.STRING
    )
    operator = EnumField(
        PromotionOperatorEnum,
        default=PromotionOperatorEnum.EQUAL,
        max_length=32,
    )
    value = models.CharField(max_length=512)
    
    def __str__(self) -> str:
        return f"{self.field} {self.operator} {self.value}"


class PromotionResult(BaseModel):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='results'
    )
    type = EnumField(
        PromotionTypeEnum,
        default=PromotionTypeEnum.DIRECT_DISCOUNT,
        max_length=32,
    )
    data_type = EnumField(
        PromotionResultDataTypeEnum,
        default=PromotionResultDataTypeEnum.STRING,
        max_length=32,
    )
    value = models.FloatField()
    
    def __str__(self) -> str:
        return f"{self.type} {self.value}"
