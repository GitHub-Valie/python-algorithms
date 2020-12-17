from collections import deque
from functions import futures_get_hist
import websocket, json
import pandas as pd
import btalib
from pprint import pprint
import numpy as np

# Pseudo code

# Variables
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
WSS_URL = "wss://fstream.binance.com"
WSS_ENDPOINT = "/ws/{}@kline_{}".format(
    SYMBOL.lower(),
    INTERVAL
)

position = 0
open_short = []
open_long = []
close_short = []
close_long = []
pnl = []

# Get historical data
historical_data = futures_get_hist(
    SYMBOL,
    INTERVAL
)

closes = deque([], maxlen=30) # where ticks will be stored

smas = deque([], maxlen=30)

for candle in historical_data:
    closes.append([float(candle[4])])

df = pd.DataFrame(data=closes, columns=['close'])

sma = btalib.sma(df, period=30)

smas.append([sma.df.to_numpy()[-1][0]])

# Get live ticks
def on_open(ws):
    print('Opened connection')

def on_close(ws):
    print('Closed connection')

def on_message(ws, message):
    global closes, smas, df, position, pnl, open_long, open_short, close_long, close_short

    tmp = deque([], maxlen=31)

    json_message = json.loads(message)
    candle = json_message["k"]

    # pseudo code: Refresh data with wss data
    # store intraperiod ticks in temporary list 'tmp'
    # if candle closed, append close price to 'closes'

    if candle['x'] == False:

        for close in list(closes): # append prices from closed candles to tmp
            tmp.append(close)
        tmp.append([float(candle['c'])]) # at last, add latest price stream to tmp
        
        df = pd.DataFrame(data=list(tmp), columns=['close']) # create a dataframe to use btalib library
        # print(df) # only last df row changes

        # calculate slow and fast sma
        fast_sma = btalib.sma(df, period=5)
        slow_sma = btalib.sma(df, period=30)
        
        print('fast sma: {}     | slow sma: {}'.format(
            round(fast_sma.df.to_numpy()[-1][0], 2),
            round(slow_sma.df.to_numpy()[-1][0], 2)
        ))

        print(round(sum(pnl), 2))

        # Strategy

        if position == 1 and float(fast_sma.df.to_numpy()[-1][0]) < slow_sma.df.to_numpy()[-1][0]: # short condition
            print('fast sma {} < slow sma {} | EXIT LONG & GO SHORT'.format(
                round(fast_sma.df.to_numpy()[-1][0], 2),
                round(slow_sma.df.to_numpy()[-1][0], 2)
            ))
            position = -1
            close_long.append(float(candle['c']))
            open_short.append(float(candle['c']))
            pnl.append(close_long[-1] - open_long[-1])
            
        elif position == -1 and float(fast_sma.df.to_numpy()[-1][0]) > slow_sma.df.to_numpy()[-1][0]: # long condition
            print('fast sma {} > slow sma {} | EXIT SHORT & GO LONG'.format(
                round(fast_sma.df.to_numpy()[-1][0], 2),
                round(slow_sma.df.to_numpy()[-1][0], 2)
            ))
            position = 1
            close_short.append(float(candle['c']))
            open_long.append(float(candle['c']))
            pnl.append(open_short[-1] - close_short[-1])

        elif position == 0: # position = 0
            # if fast_sma crosses over slow_sma: go long
            if float(fast_sma.df.to_numpy()[-1][0]) > slow_sma.df.to_numpy()[-1][0]:
                print('fast sma {} > slow sma {} | GO LONG'.format(
                    round(fast_sma.df.to_numpy()[-1][0], 2),
                    round(slow_sma.df.to_numpy()[-1][0], 2)
                ))
                position = 1
                open_long.append(float(candle['c']))

            # elif fast_sma crosses under slow_sma: go short
            elif float(fast_sma.df.to_numpy()[-1][0]) < slow_sma.df.to_numpy()[-1][0]:
                print('fast sma {} < slow sma {} | GO SHORT'.format(
                    round(fast_sma.df.to_numpy()[-1][0]),
                    round(slow_sma.df.to_numpy()[-1][0])
                ))
                position = -1
                open_short.append(float(candle['c']))

            # none of these
            else:
                pass

        else: # position != 0, -1, 1
            pass

    else: # Edit condition to append last data and pop it, except if candle is closed

        closes.append([float(candle['c'])])

        df = pd.DataFrame(data=closes, columns=['close'])

        fast_sma = btalib.sma(df, period=5)
        slow_sma = btalib.sma(df, period=30)

        # Strategy

        if position == 1 and float(fast_sma.df.to_numpy()[-1][0]) < slow_sma.df.to_numpy()[-1][0]: # short condition
            print('fast sma {} < slow sma {} | EXIT LONG & GO SHORT'.format(
                round(fast_sma.df.to_numpy()[-1][0], 2),
                round(slow_sma.df.to_numpy()[-1][0], 2)
            ))
            position = -1
            close_long.append(float(candle['c']))
            open_short.append(float(candle['c']))
            pnl.append(close_long[-1] - open_long[-1])
            
        elif position == -1 and float(fast_sma.df.to_numpy()[-1][0]) > slow_sma.df.to_numpy()[-1][0]: # long condition
            print('fast sma {} > slow sma {} | EXIT SHORT & GO LONG'.format(
                round(fast_sma.df.to_numpy()[-1][0], 2),
                round(slow_sma.df.to_numpy()[-1][0], 2)
            ))
            position = 1
            close_short.append(float(candle['c']))
            open_long.append(float(candle['c']))
            pnl.append(open_short[-1] - close_short[-1])

        elif position == 0: # position = 0
            # if fast_sma crosses over slow_sma: go long
            if float(fast_sma.df.to_numpy()[-1][0]) > slow_sma.df.to_numpy()[-1][0]:
                print('fast sma {} > slow sma {} | GO LONG'.format(
                    round(fast_sma.df.to_numpy()[-1][0], 2),
                    round(slow_sma.df.to_numpy()[-1][0], 2)
                ))
                position = 1
                open_long.append(float(candle['c']))

            # elif fast_sma crosses under slow_sma: go short
            elif float(fast_sma.df.to_numpy()[-1][0]) < slow_sma.df.to_numpy()[-1][0]:
                print('fast sma {} < slow sma {} | GO SHORT'.format(
                    round(fast_sma.df.to_numpy()[-1][0], 2),
                    round(slow_sma.df.to_numpy()[-1][0], 2)
                ))
                position = -1
                open_short.append(float(candle['c']))

            # else do nothing
            else:
                pass

        else: # position != 0, -1, 1
            pass

# Websocket App
while True:
    ws = websocket.WebSocketApp(
        WSS_URL + WSS_ENDPOINT,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()