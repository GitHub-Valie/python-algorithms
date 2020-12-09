# Based on basic_live_algo.py, this algorithm's trading strategy 
# is different in that it will take LONG / SHORT on a basket of 
# technical indicators instead of a "simple" SMA strategy

# Imports
import json, requests, websocket
from pprint import pprint
import numpy as np


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
ups = []
downs = []
rsi_list = []
bb_list = []
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


# Technical indicators

# Trend indicators
def sma(arr, window):
    '''
    Standard Moving Average     
    :arr: array     
    :window: window on which SMA will be calculated     
    '''
    return np.convolve(arr, np.ones(window), 'valid') / window


def ewma(arr, alpha, window):
    '''
    Exponential Weighted Moving Average     
    :arr: array     
    :param alpha: specify decay [0, 1]      
    :window: length of ewma 
    '''
    arr = arr[-(len(arr) - window + 1):] # Re-adjusting length of arr so it has the same len as sma
    ewma_arr = np.zeros_like(arr) # returns an array of zeros the same length as arr
    ewma_arr[0] = arr[0] # first value in list ewma_arr is equal to first value in list arr
    for t in range(1, arr.shape[0]):
        ewma_arr[t] = alpha * arr[t] + (1 - alpha) * ewma_arr[t - 1]
    
    return ewma_arr


# Momentum indicators
def rsi(ups_list, downs_list, n):
    '''
    Relative Strength Index     
    rsi < 30 : oversold     
    rsi > 70 : overbought
    '''
    gains = ewma(
        arr=np.array(ups_list),
        window=n,
        alpha=2 / (1 + n)
    )

    losses = ewma(
        arr=np.array(downs_list),
        window=n,
        alpha=2 / (1+n)
    )

    RSI = gains[-n:] / (gains[-n:] + abs(losses[-n:])) * 100

    return RSI[-1]


# Volatility indicators
def bbands(arr, window):
    '''
    Bollinger Bands. Given an array and a certain timeframe (window), returns:      
    `bb_mid` : simple moving average    
    `bb_top` : bb_mid + 2 standard devs     
    `bb_bot` : bb_mid - 2 standard devs     
        
    params:     
    :arr: array, list object    
    :window: int    
    '''
    bb_mid = sma(
        arr,
        window
    )[-1]

    bb_top = bb_mid + 2 * np.std(
        arr,
        ddof=1
    )

    bb_bot = bb_mid - 2 * np.std(
        arr,
        ddof=1
    )

    bollingerbands = [
        bb_bot,
        bb_mid,
        bb_top
    ]

    return bollingerbands


# Websocket functions
def on_open(ws):
    print("Opened Connection: ", WSS_BASE_URL + WSS_ENDPOINT)
    # Get historical data
    historical_data = futures_get_hist(
        symbol=SYMBOL,
        interval=INTERVAL
    )

    # Create data and closes list
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

    # Calculate price deltas
    for i in range(len(historical_data)): # For i ∈ [0, len(historical_data)]
        delta = float(historical_data[i+1][4]) - float(historical_data[i][4])

        if delta > 0: # if price went up, append to ups
            ups.append(delta)
        elif delta < 0: # if price went down, append to downs
            downs.append(delta)
        else:
            pass


def on_close(ws):
    print("Closed connection")


def on_message(ws, message):
    global data, closes, ups, downs, rsi_list, bb_list, position

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
        data.pop(-1), closes.pop(-1) # delete last data, close list elements
        data.append(kline), closes.append(kline[4]) # update lists with the fresh ws data
        
        # Calculate 'close' price change
        delta = float(closes[-1]) - float(closes[-2])
        if delta > 0:
            ups.pop(-1)
            ups.append(delta)
        elif delta < 0:
            downs.pop(-1)
            downs.append(delta)
        else:
            pass

        
    # if kline open timestamp has changed: 
    else:
        print("Timestamp has changed")
        data.pop(0), closes.pop(0) # for each list, delete oldest list element
        data.append(kline), closes.append(kline[4]) # append new wss data to respective lists

        # Calculate 'close' price change
        delta = float(closes[-1]) - float(closes[-2])
        if delta > 0:
            ups.pop(-1)
            ups.append(delta)
        elif delta < 0:
            downs.pop(-1)
            downs.append(delta)
        else:
            pass

    boll = bbands(
        arr=closes,
        window=200
    )

    RSI = rsi(
        ups_list=ups,
        downs_list=downs,
        n=26
    )

    print(
        '\nClose: {}'.format(round(closes[-1], 2)),
        '\nBB Bot: {}\nBB Mid: {}\nBB Top: {}'.format(
            round(boll[0], 2),
            round(boll[1], 2),
            round(boll[2], 2)
        ),
        '\nRSI: {}'.format(RSI)
    )


# WebSocketApp        
while True:
    ws = websocket.WebSocketApp(
        WSS_BASE_URL + WSS_ENDPOINT,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()