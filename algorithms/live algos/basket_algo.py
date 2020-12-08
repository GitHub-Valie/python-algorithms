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
# Trend
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


# Momentum
def rsi():
    return rsi

def macd():
    return macd

# Volatility
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
        window=window
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


# WebSocketApp
