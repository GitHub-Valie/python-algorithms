# Imports
from collections import deque
from functions import futures_get_hist
from portfolio import portfolio
from algorithm import Algorithm
import websocket, json
from pprint import pprint

# Variables
bots = []
WSS_URL = "wss://fstream.binance.com"

for asset in portfolio:
    bots.append(asset)
    bots[-1]['bot'] = Algorithm(
        asset['pair'],
        asset['interval']
    )

    WSS_ENDPOINT = "/ws/{}@kline_{}".format(
        asset['pair'].lower(),
        asset['interval']
    )

    WSS_URL += WSS_ENDPOINT
    print(WSS_URL)

# Get live data: websocket app
def on_open(ws):
    print('Open')

def on_close(ws):
    print('Close')

def on_message(ws, message):
    json_message = json.loads(message)
    data = json_message['k']
    # print(data)
    for bot in bots:
        if bot['pair'] == data['s']:
            bot['bot'].next(data)
            break

    # Pass it through the algorithm

while True:
    ws = websocket.WebSocketApp(
        WSS_URL,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()
