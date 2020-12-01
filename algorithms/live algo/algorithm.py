from portfolio import portfolio
import requests

# TODO: Add klines (request historical data)
# TODO: create function "next"

class Algorithm:
    def __init__(self, Asset, Weight, Period):
        self.asset = Asset
        self.weight = Weight
        self.period = Period
        self.data = [] # list or dataframe?
        hist = requests.get(
            "https://fapi.binance.com" + "/fapi/v1/klines",
            params = {
                'symbol': Asset,
                'interval': '1h'
            }
        )
        hist = hist.json()
        for i in range(len(hist)):
            if len(self.data) < self.period:
                self.data.append({
                    'time_open' : hist[i][0],
                    'open' : hist[i][1],
                    'high' : hist[i][2],
                    'low' : hist[i][3],
                    'close' : hist[i][4],
                    'time_close' : hist[i][6] 
                    # Add special TA indicators like SMA here
                })
            
            else:
                self.data.append({
                    'time_open' : hist[i][0],
                    'open' : hist[i][1],
                    'high' : hist[i][2],
                    'low' : hist[i][3],
                    'close' : hist[i][4],
                    'time_close' : hist[i][6] 
                    # Add special TA indicators like SMA here
                })

    def next(self, candle):
        if candle['t'] != self.data[-1]['time_open']:
            self.data.pop(0)
            self.data.append({
                'time_open' : candle['t'],
                'open' : candle['o'],
                'high' : candle['h'],
                'low' : candle['l'],
                'close' : candle['c'],
                'time_close' : candle['T'] 
            })
        
        else:
            self.data[-1] = {
                'time_open' : candle['t'],
                'open' : candle['o'],
                'high' : candle['h'],
                'low' : candle['l'],
                'close' : candle['c'],
                'time_close' : candle['T'] 
            }

        print(self.asset, len(self.data))
