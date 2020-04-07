from enum import Enum


class PayopApiException(Exception):
    pass


class PayopValidationException(Exception):
    pass

class Language(Enum):
    EN = 'en'
    RU = 'ru'


class TransactionStatus(Enum):
    NEW = 1
    ACCEPTED = 2
    PENDING = 4
    FAILED = 3, 5


class RefundType(Enum):
    FULL = 1
    PARTIAL = 2
