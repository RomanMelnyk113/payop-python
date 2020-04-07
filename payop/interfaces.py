from dataclasses import dataclass
from typing import Optional

from payop import Language, RefundType


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


@dataclass
class RefundBody:
    transactionIdentifier: str
    refundType: RefundType

    amount: Optional[str] = None


@dataclass
class RefundResponse:
    status: int
    data: str


@dataclass
class Transaction:
    identifier: str
    walletIdentifier: str
    type: str
    amount: float
    currency: str
    payAmount: float
    payCurrency: str
    state: int
    createdAt: int

    chosenCurrency: Optional[str] = None
    chosenAmount: Optional[float] = None
    error: Optional[str] = None
    cardMetadata: Optional[dict] = None
    commission: Optional[list] = None
    exchange: Optional[list] = None
    updatedAt: Optional[str] = None
    orderId: Optional[str] = None
    description: Optional[str] = None
    productAmount: Optional[str] = None
    productCurrency: Optional[str] = None
    pageDetails: Optional[str] = None
    language: Optional[str] = None
    paymentMethodIdentifier: Optional[str] = None
    payerInformation: Optional[list] = None
    refunds: Optional[list] = None
    chargeBacks: Optional[list] = None
    geoInformation: Optional[dict] = None
    resultUrl: Optional[str] = None
    failUrl: Optional[str] = None
    pid: Optional[str] = None
    application: Optional[dict] = None
    strategy: Optional[int] = None
