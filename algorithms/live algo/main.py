import json
from pprint import pprint

import websocket

from algorithm import Algorithm
from portfolio import portfolio

# TODO: Create an algorithm that takes decisions in real time

BASE_URL = "wss://fstream3.binance.com/stream?streams="

# Create algorithms for each asset
algorithms = []
for cryptocurrency in portfolio:
    algorithms.append(cryptocurrency)
    algorithms[-1]['algorithm'] = Algorithm(
        cryptocurrency['Asset'],
        cryptocurrency['Weight']
    )
    BASE_URL += cryptocurrency['Asset'].lower() + "@kline_1m/"

# Connect to websocket
def on_open(ws):
    print("Opened connection")

def on_close(ws):
    print("Closed connection")

def on_message(ws, message):
    message = json.loads(message)
    data = message['data']['k']
    for algorithm in algorithms:
        if algorithm['Asset'] == data['s']:
            algorithm['algorithm']

while True:
    ws = websocket.WebSocketApp(
        BASE_URL,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()

# Decision

# Summary

# Extract

# {'data': {'E': 1606844798542,
#           'e': 'kline',
#           'k': {'B': '0', # Ignore
#                 'L': 298229697,
#                 'Q': '1440378.47073',
#                 'T': 1606844819999, # Close time
#                 'V': '76.714',
#                 'c': '18776.23', # Close
#                 'f': 298228663,
#                 'h': '18799.97', # High
#                 'i': '1m', # interval
#                 'l': '18756.15', # Low
#                 'n': 1035, # Number of trades
#                 'o': '18799.97', # Open
#                 'q': '3415292.39370',
#                 's': 'BTCUSDT', # Symbol
#                 't': 1606844760000, # Open time
#                 'v': '181.879', 
#                 'x': False}, # Is candle closed?
#           's': 'BTCUSDT'},
#  'stream': 'btcusdt@kline_1m'}
# {'data': {'E': 1606844798702,
#           'e': 'kline',
#           'k': {'B': '0',
#                 'L': 169545179,
#                 'Q': '465748.74867',
#                 'T': 1606844819999,
#                 'V': '789.745',
#                 'c': '589.82',
#                 'f': 169544357,
#                 'h': '590.71',
#                 'i': '1m',
#                 'l': '588.78',
#                 'n': 823,
#                 'o': '590.66',
#                 'q': '1363040.45299',
#                 's': 'ETHUSDT',
#                 't': 1606844760000,
#                 'v': '2311.180',
#                 'x': False},
#           's': 'ETHUSDT'},
#  'stream': 'ethusdt@kline_1m'}
      