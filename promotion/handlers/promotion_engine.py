from typing import List, Dict, Any

from promotion import enums, models
from user.models import UserMembership


class PromotionEngine:
    def __init__(self, order: Any):
        self.order = order
        self.promotions = models.Promotion.objects.filter(is_enabled=True)

    def check_conditions(self, conditions: List[Dict[str, Any]]) -> bool:
        for condition in conditions:
            if not self.check_condition(condition):
                return False
        return True
    
    def check_condition(self, condition: Dict[str, Any]) -> bool:
        data_type = condition.data_type
        if data_type == enums.PromotionConditionFieldDataTypeEnum.ID:
            return self._check_condition_with_id(condition)
        else:
            raise ValueError('Invalid data type')

    def _check_condition_with_id(self, condition: Dict[str, Any]) -> bool:
        field = condition.field.upper()
        operator = condition.operator.upper()

        try:
            value = int(condition.value)
        except:
            raise ValueError('Invalid value type')
        
        if field == enums.PromotionConditionFieldEnum.PRODUCT.value:
            for item in self.order.order_items.all():
                if self.evaluate_condition(item.product.id, operator, value):
                    return True
            return False
        elif field == enums.PromotionConditionFieldEnum.MEMBERSHIP.value:
            user_membership = UserMembership.objects.filter(
                user=self.order.user,
                is_enabled=True
            ).first()
            
            if not user_membership:
                return False
            if self.evaluate_condition(user_membership.membership.id, operator, value):
                return True

        return False

    def evaluate_condition(self,
                        field_value: Any,
                        operator: enums.PromotionOperatorEnum,
                        condition_value: Any) -> bool:
        if operator == enums.PromotionOperatorEnum.EQUAL:
            return field_value == condition_value
        elif operator == enums.PromotionOperatorEnum.NOT_EQUAL:
            return field_value != condition_value

        return False

    def apply_promotion(self) -> float:
        total_discount = 0.0
        for promotion in self.promotions:
            for group in promotion.condition_groups.all():
                if group.operator == enums.PromotionGroupOperatorEnum.AND:
                    if self.check_conditions(group.conditions.all()):
                        return total_discount + self.apply_results(promotion.results.all())
                elif group.operator == enums.PromotionGroupOperatorEnum.OR:
                    if any(self.check_conditions([cond]) for cond in group.conditions.all()):
                        return total_discount + self.apply_results(promotion.results.all())
        return total_discount

    def apply_results(self, results: List[models.PromotionResult]) -> float:
        discount = 0.0
        for result in results:
            if result.type == enums.PromotionTypeEnum.DIRECT_PERCENTAGE:
                discount += self.order.origin_total_amount * float(result.value) / 100
            elif result.type == enums.PromotionTypeEnum.DIRECT_DISCOUNT:
                discount += float(result.value)
            else:
                raise ValueError('Invalid promotion type')

        return discount
