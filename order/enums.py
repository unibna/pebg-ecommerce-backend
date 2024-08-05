from base.enums import BaseEnum


class OrderStatusEnum(str, BaseEnum):
    DRAFT = 'Draft'
    PAYMENT_COMPLETED = 'Payment Completed'
    PROCESSING = 'Processing'
    DELIVERING = 'Delivering'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
