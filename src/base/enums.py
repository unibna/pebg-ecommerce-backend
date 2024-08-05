from enum import Enum

class BaseEnum(Enum):

    @classmethod
    def values(cls, excludes=[]):
        return [field.value for field in cls if field.value not in excludes]
    
    @classmethod
    def parse(cls, values):
        fields = []
        for value in values:
            for field in cls:
                if field.value == value:
                    fields.append(field)
        return fields
    
    @classmethod
    def is_valid_values(cls, values):
        return all(value in cls.values() for value in values)


    @classmethod
    def from_string(cls, value):
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"Invalid enum value: {value}")
