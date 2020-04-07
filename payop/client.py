import dataclasses
import logging
from hashlib import sha256
import json
from http import HTTPStatus
from typing import Optional, List

import requests

from . import PayopApiException, Language, PayopValidationException
from .interfaces import (Invoice, InvoiceResponse, CallbackResponse, CallbackInvoice,
                         CallbackTransaction, CallbackOrder, CallbackError, RefundBody,
                         RefundResponse, Transaction)

DEFAULT_BASE_API_URL = 'https://payop.com'
CHECKOUT_PAGE = "https://payop.com/{locale}/payment/invoice-preprocessing/{invoice_id}"
CREDIT_CARD_PAYMENT_METHOD_ID = 381

logger = logging.getLogger(__name__)


class Payop:

    def __init__(self, token: str, public_key: str, secret_key: str = None, api_url=None):
        self.access_token = token
        self.secret_key = secret_key
        self.public_key = public_key

        self.api_url = api_url or DEFAULT_BASE_API_URL

    def _create_signature(self, order_id, amount, currency):
        m = sha256(f"{amount}:{currency}:{order_id}:{self.secret_key}".encode())
        return m.hexdigest()

    def _check_signature(self, signature, callback_signature):
        return callback_signature == signature

    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _send_request(
            self,
            endpoint: str,
            data: Optional[dict] = None,
            method: str = "get"
    ) -> dict:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        method_to_call = getattr(requests, method)
        r = method_to_call(self._generate_url(endpoint), headers=headers, json=data)
        print(r.text)
        if r.status_code != HTTPStatus.OK:
            raise PayopApiException(
                'Payop error: {}. Error code: {}'.format(r.text, r.status_code))

        return json.loads(r.text)

    def _create_invoice(self, data: Invoice) -> InvoiceResponse:
        '''
        Create new invoice data
        https://github.com/Payop/payop-api-doc/blob/master/Invoice/createInvoice.md#create-invoice

        :param data: Relevant data to create new invoice
        :return: InvoiceResponse

        Payop API response
        Example: {
            "data": "",
            "status": 1
        }
        '''

        endpoint = '/v1/invoices/create'

        data_to_send = dataclasses.asdict(data)
        data_to_send["publicKey"] = self.public_key
        data_to_send["signature"] = self._create_signature(
            order_id=data.order.id, currency=data.order.currency, amount=data.order.amount
        )
        if data_to_send["order"]["items"] is None:
            data_to_send["order"]["items"] = []
        # TODO: error handling
        response = self._send_request(endpoint, data_to_send, method="post")
        return InvoiceResponse(
            data=response["data"], status=response["status"]
        )

    def get_available_methods(self) -> List[dict]:
        endpoint = '/v1/instrument-settings/payment-methods/available-for-user'
        response = self._send_request(endpoint)
        return response["data"]

    def get_transaction(self, transaction_id: str) -> Transaction:
        """
        Fetch transaction:

        :param transaction_id:
        :return:
        """
        endpoint = '/v1/transactions/{id}'
        response = self._send_request(endpoint.format(id=transaction_id))
        return Transaction(**response['data'])

    def checkout(self, data: Invoice) -> str:
        '''
        Perform checkout action and return hosted checkout page URL

        :argument data:Invoice - Invoice data
        :returns checkout URL
        :raises PayopApiException - on API error
        '''

        invoice_res = self._create_invoice(data)
        return CHECKOUT_PAGE.format(locale=Language.EN.value, invoice_id=invoice_res.data)

    def refund(self, data: RefundBody) -> RefundResponse:
        '''
            Refund transaction
            https://github.com/Payop/payop-api-doc/blob/master/refund.md

            :param data: Refund data
            :return: InvoiceResponse

            Payop API response
            Example: {
                "data": "",
                "status": 1
            }
        '''

        endpoint = '/v1/refunds/create'
        data_to_send = dataclasses.asdict(data)
        response = self._send_request(endpoint, data_to_send, method="post")
        return RefundResponse(status=response.get("status"), data=response.get("data"))

    def parse_callback_data(self, data: dict) -> CallbackResponse:
        '''
        Parse and validate IPN data

        :raises PayopValidationException
        '''
        try:
            return CallbackResponse(
                invoice=CallbackInvoice(
                    id=data["invoice"]["id"],
                    txid=data["invoice"]["txid"],
                    metadata=data["invoice"]["metadata"],
                ),
                transaction=CallbackTransaction(
                    id=data["transaction"]["id"],
                    state=data["transaction"]["state"],
                    order=CallbackOrder(id=data["transaction"]["order"]["id"]),
                    error=CallbackError(
                        message=data["transaction"]["error"]["message"],
                        code=data["transaction"]["error"]["code"]
                    ),
                )
            )
        except TypeError as e:
            msg = f"Error during Payop callback data parsing: {str(e)}"
            logger.error(msg)
            raise PayopValidationException(msg)
