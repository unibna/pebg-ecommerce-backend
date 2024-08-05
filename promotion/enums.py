from base.enums import BaseEnum


class PromotionTypeEnum(str, BaseEnum):
    DIRECT_DISCOUNT = 'DIRECT_DISCOUNT'
    DIRECT_PERCENTAGE = 'DIRECT_PERCENTAGE'
    
    
class PromotionResultDataTypeEnum(str, BaseEnum):
    STRING = 'STRING'
    INTEGER = 'INT'
    FLOAT = 'FLOAT'
    ID = 'ID'
    
    
class PromotionConditionFieldEnum(str, BaseEnum):
    PRODUCT = 'PRODUCT'
    MEMBERSHIP = 'MEMBERSHIP'
    
    
class PromotionConditionFieldDataTypeEnum(str, BaseEnum):
    STRING = 'STRING'
    INTEGER = 'INT'
    FLOAT = 'FLOAT'
    ID = 'ID'


class PromotionOperatorEnum(str, BaseEnum):
    # Common
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    
    # Number
    GREATER_THAN = 'GREATER_THAN'
    GREATER_THAN_EQUAL = 'GREATER_THAN_EQUAL'
    LESS_THAN = 'LESS_THAN'
    LESS_THAN_EQUAL = 'LESS_THAN_EQUAL'
    
    # String
    CONTAINS = 'CONTAINS'
    NOT_CONTAINS = 'NOT_CONTAINS'
    STARTS_WITH = 'STARTS_WITH'
    ENDS_WITH = 'ENDS_WITH'
    
    
class PromotionGroupOperatorEnum(str, BaseEnum):
    AND = 'AND'
    OR = 'OR'
