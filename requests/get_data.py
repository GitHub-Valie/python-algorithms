import requests
from pprint import pprint
import csv

BASE_URL = "https://api.binance.com"
SYMBOL = "BTCUSDT"

# Request OHLC data on BTCUSDT
req = requests.get(
    BASE_URL + "/api/v3/klines",
    params={
        'symbol': SYMBOL,
        'interval': '1m'
    }
)

# Open a .csv file and write data in it
csvfile = open(
    'data\{}.csv'.format(SYMBOL), 
    'w', 
    newline=''
)

data_writer = csv.writer(
    csvfile, 
    delimiter=','
)

writer = csv.DictWriter(
    csvfile,
    fieldnames=[
        'Datetime', 
        'Open', 
        'High', 
        'Low', 
        'Close', 
        'Volume', 
        'Close time', 
        'Quote asset volume', 
        'Number of trades', 
        'Taker BUY base asset volume', 
        'Taker BUY quote asset volume', 
        'Ignore'
    ]
)

writer.writeheader()

candlesticks = req.json()

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    data_writer.writerow(candlestick)

csvfile.close()
