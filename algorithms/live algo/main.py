import json
from pprint import pprint

import websocket

from algorithm import Algorithm
from portfolio import portfolio

# TODO: 
# DONE: A portfolio of multiple currencies (portfolio.py)
# DONE: Historical and live data requesting (main.py : WebSocketApp)
# Decision tree based on a basket technical indicators
# Technical Indicators
# Basket
# Decision tree
# Summary/performance tracking: define variables (pnl, counters, buysell, profit, winrate, ...)
# Portfolio rebalancing

BASE_URL = "wss://fstream3.binance.com/stream?streams="

# Create algorithms for each asset
algorithms = []
for cryptocurrency in portfolio:
    algorithms.append(cryptocurrency)
    # Create one instance of "Algorithm" for each cryptocurrency in portfolio
    algorithms[-1]['algorithm'] = Algorithm(
        cryptocurrency['Asset'],
        cryptocurrency['Weight'],
        cryptocurrency['Period']
    )
    BASE_URL += cryptocurrency['Asset'].lower() + "@kline_1h/"

# Connect to websocket
def on_open(ws):
    print("Opened connection")

def on_close(ws):
    print("Closed connection")

def on_message(ws, message):
    message = json.loads(message)
    data = message['data']['k']
    # pprint(data)
    for instance in algorithms:
        if instance['Asset'] == data['s']:
            instance['algorithm'].next(data)
            break

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
      