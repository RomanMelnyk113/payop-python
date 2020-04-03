from dataclasses import dataclass
from typing import Optional

from payop import Language


@dataclass
class Order:
    id: str
    amount: str
    currency: str
    description: str

    items: Optional[list] = None


@dataclass
class Payer:
    email: str

    name: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class Invoice:
    order: Order
    payer: Payer
    resultUrl: str
    failPath: str
    paymentMethod: str

    language: Language = Language.EN.value
    metadata: Optional[dict] = None


@dataclass
class InvoiceResponse:
    data: str
    status: int
