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


@dataclass
class CallbackInvoice:
    id: str
    txid: str
    metadata: Optional[dict] = None


@dataclass
class CallbackError:
    message: str
    code: str

@dataclass
class CallbackOrder:
    id: str


@dataclass
class CallbackTransaction:
    id: str
    state: int
    order: CallbackOrder
    error: Optional[CallbackError] = None

@dataclass
class CallbackResponse:
    invoice: CallbackInvoice
    transaction: CallbackTransaction
