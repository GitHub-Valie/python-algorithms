# This algorithm is a websocket app
# 1/ Request historical data
# 2/ Connect to a websocket stream
# 3/ Process live data and perform technical analysis (sma)
# 4/ Take action: buy, sell, hold (do nothing)

import json, requests, websocket
import numpy as np
from pprint import pprint

# Define variables
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
WSS_BASE_URL = "wss://fstream.binance.com"
WSS_ENDPOINT = "/ws/{}@kline_{}".format(
    SYMBOL.lower(),
    INTERVAL
)
data = []
closes = []
position = 0

# Function to get historical data
def futures_get_hist(symbol, interval):
    '''
    Get historical klines for a futures pair    
    :symbol: str, i.e "BTCUSDT"     
    :interval: str, i.e "1m"    
    '''
    r = requests.get(
        "https://fapi.binance.com" + "/fapi/v1/klines",
        params = {
            'symbol': symbol,
            'interval': interval
        }
    )

    req = r.json()
    return req

# Technical indicator: Standard Moving Average
def sma(arr, window):
    return np.convolve(arr, np.ones(window), 'valid') / window

# Websocket functions
def on_open(ws):
    print("Opened Connection: ", WSS_BASE_URL + WSS_ENDPOINT)
    historical_data = futures_get_hist(
        symbol=SYMBOL,
        interval=INTERVAL
    )

    for candle in historical_data:
        candle = [
            float(candle[0]),
            float(candle[1]),
            float(candle[2]),
            float(candle[3]),
            float(candle[4]),
            float(candle[5]),
            float(candle[8]),
            float(candle[6])
        ]
        data.append(candle)
        closes.append(candle[4])


def on_close(ws):
    print("Closed connection")


def on_message(ws, message):
    global data, closes, position

    json_message = json.loads(message)
    candle = json_message['k']
    kline = [
        float(candle['t']),
        float(candle['o']),
        float(candle['h']),
        float(candle['l']),
        float(candle['c']),
        float(candle['v']),
        float(candle['n']),
        float(candle['T'])
    ]

    # if kline open timestamp = last data's candle's timestamp:
    if kline[0] == data[-1][0]:
        data.pop(-1)
        closes.pop(-1) # delete last data, close list elements
        data.append(kline)
        closes.append(kline[4]) # update lists with the fresh ws data
        
    # if kline open timestamp has changed: 
    else:
        print("Timestamp has changed")
        data.pop(0)
        closes.pop(0) # for each list, delete oldest list element
        data.append(kline)
        closes.append(kline[4]) # append new wss data to respective lists

    # Put technical indicator calculation here
    sma_200 = sma(
        arr=closes,
        window=200
    )

    print(
        '   200 minutes SMA: {}\n'.format(round(sma_200[-1], 2)),
        '  Close:           {}'.format(round(closes[-1], 2))
    )

    # Strategy: go long if SMA > last close ; go short if SMA < last close
    if position == 0: # No position yet
        
        if sma_200[-1] > closes[-1]: # Long condition is met
            position = 1
            print('SMA_200 > Last close: GO LONG')
    
        elif sma_200[-1] < closes[-1] and position == 0: # Short condition is met
            position = -1
            print('SMA_200 < Last close: GO SHORT')
        
        else: # Not long neither short condition met
            pass
    
    elif position == 1: # Long position
        
        if sma_200[-1] < closes[-1]: # Short position is met
            position = -1
            print('SMA_200 < Last close: CLOSE LONG & GO SHORT')

        else:
            pass

    else: # Short position
        
        if sma_200[-1] > closes[-1]: # Long condition is met
            position = 1
            print('SMA_200 > Last close: CLOSE SHORT & GO LONG')

        else:
            pass

# WebSocketApp        
while True:
    ws = websocket.WebSocketApp(
        WSS_BASE_URL + WSS_ENDPOINT,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()