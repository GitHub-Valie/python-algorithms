import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode

BASE_URL = 'https://api.binance.com'

# Two types of requests : public or signed

# Public requests do not require public and secret keys

def dispatch_request(http_method)

def send_public_request():
    return response