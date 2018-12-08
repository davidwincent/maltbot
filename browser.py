"""browse the world wide web and multimedia"""
import os
from urllib.parse import urlencode, quote_plus, unquote
from urllib3.contrib.socks import SOCKSProxyManager
import urllib3
import certifi

SOCKS_PROXY = os.environ["SOCKS_PROXY"]

HTTP = urllib3.PoolManager(
    num_pools=50,
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where())
PROXY = SOCKSProxyManager(SOCKS_PROXY)


def url_encode(value):
    """url encode value using urllib.parse"""
    return urlencode(value, quote_via=quote_plus)


def url_decode(value):
    """url decode value using urllib.parse"""
    return unquote(value)


def http_validate(response, valid_status=200):
    """validate http response"""
    if response.status == valid_status:
        return True
    raise HttpError({
        "message": "HTTP error %(status)i" % {"status": response.status},
        "status": response.status})


class HttpError(Exception):
    """HttpError Exception"""

    def __init__(self, details):
        super().__init__(details["message"])
