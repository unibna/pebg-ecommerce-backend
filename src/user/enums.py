from base.enums import BaseEnum


class UserRoleEnum(str, BaseEnum):
    CUSTOMER = 'customer'
    STAFF = 'staff'
