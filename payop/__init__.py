from enum import Enum


class PaymentException(Exception):
    pass

class Language(Enum):
    EN = 'en'
    RU = 'ru'