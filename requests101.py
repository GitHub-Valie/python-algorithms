# This program sends a request to Binance servers and prints the server time in datetime format

import requests
from datetime import datetime

BASE_URL = "https://api.binance.com"

req = requests.get(
    BASE_URL + '/api/v3/time'
)

print(
    datetime.fromtimestamp(
        round(req.json()['serverTime'] / 1000)
    )
)