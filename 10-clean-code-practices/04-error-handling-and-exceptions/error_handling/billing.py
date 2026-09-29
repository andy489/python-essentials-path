"""
billing.py
-----------

This Mock module handles billing, such as charging users
and managing their subscription plans.
"""


class NetworkTimeout(Exception):
    pass


class HTTPError(Exception):
    pass


def charge_new_user(username: str):
    pass


class SwiftPaymentProviderError(Exception):
    pass


class BillingFailedException(Exception):
    pass


class CreditCardDeclinedException(BillingFailedException):
    pass


class NoBillingInfoException(BillingFailedException):
    pass


class SwiftPaymentGatewayException(BillingFailedException):
    pass


class AccountNumberInvalidException(BillingFailedException):
    pass


def make_swift_payment(account, amount):
    try:
        con = swift.connect()
        con.transfer_amount(account, amount)
    except (NetworkTimeout, HTTPError, SwiftPaymentProviderError) as e:
        raise SwiftPaymentGatewayException from e


# Below are mock classes for swift and connection

from dataclasses import dataclass


@dataclass
class Connection:
    def transfer_amount(self, account, amount):
        return self


@dataclass
class Swift:
    con: Connection = None

    def connect(self):
        self.con = Connection()
        return self.con


swift = Swift()
