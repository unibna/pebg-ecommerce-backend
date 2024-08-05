from base.enums import BaseEnum


class OrderStatusEnum(str, BaseEnum):
    DRAFT = 'Draft'
    PAYMENT_PENDING = 'Payment Pending'
    PAYMENT_COMPLETED = 'Payment Completed'
    PROCESSING = 'Processing'
    DELIVERING = 'Delivering'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
