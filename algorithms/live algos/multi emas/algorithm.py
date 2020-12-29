# Imports
from collections import deque
from portfolio import portfolio
from functions import futures_get_hist
from pprint import pprint
import pandas as pd

# Implement technical analysis
from ta.utils import dropna
from ta.trend import EMAIndicator

class Algorithm:

    def __init__(self, symbol, interval, weight):
        self.symbol = symbol
        self.interval = interval
        self.weight = weight
        self.data = deque([], maxlen=500)
        self.tmp = deque([], maxlen=500)
        self.position = 0
        self.pnl = []
        self.fees = []
        self.profit_counter = 0
        self.open_long = []
        self.open_short = []
        self.close_long = []
        self.close_short = []

        historical_data = futures_get_hist(
            symbol = symbol,
            interval = interval
        )

        for candle in historical_data:
            self.data.append(float(candle[4]))
    
    def get_ticks(self, candle):

        start_cash = 100

        # When candle is open, append all data from self.data in tmp list and append tick data candle['c'] to tmp
        if candle['x'] == False:
            for close in list(self.data):
                self.tmp.append(close)
            self.tmp.append(float(candle['c']))

            df = pd.DataFrame(
                data = list(self.tmp),
                columns = ['close']
            )

            emas_Used = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

            for x in emas_Used:
                ema = x
                indicator_ema = EMAIndicator(
                    close=df['close'],
                    window=x,
                    fillna=False
                )
                df['ema_' + str(ema)] = indicator_ema.ema_indicator()

            price = float(df['close'].iloc[-1])

            for i in df.index:
                c_min = min(
                    df['ema_3'][i], 
                    df['ema_5'][i], 
                    df['ema_8'][i], 
                    df['ema_10'][i], 
                    df['ema_12'][i],
                    df['ema_15'][i],
                )
                c_max = max(
                    df['ema_30'][i], 
                    df['ema_35'][i], 
                    df['ema_40'][i], 
                    df['ema_45'][i], 
                    df['ema_50'][i],
                    df['ema_60'][i],
                )

            # Positions
            if self.position == 0:

                # Entry point when short term emas > long term emas
                if c_min > c_max:
                    print('GO LONG')
                    self.position = 1
                    self.open_long.append(price)

                # Short condition is met
                elif c_max > c_min:
                    print('GO SHORT')
                    self.position = -1
                    self.open_short.append(price)

                else:
                    pass

            elif self.position == 1:

                # Short condition is met
                if c_max > c_min:
                    print('CLOSE LONG AND GO SHORT')
                    self.position = -1
                    self.close_long.append(price)
                    self.open_short.append(price)
                    self.fees.append(self.close_long[-1] * 0.01)
                    self.pnl.append(self.open_long[-1] - self.close_long[-1])

                else:
                    pass

            elif self.position == -1:

                # Long condition is met
                if c_min > c_max:
                    print('CLOSE SHORT AND GO LONG')
                    self.position = 1
                    self.close_short.append(price)
                    self.open_long.append(price)
                    self.pnl.append(self.close_short[-1] - self.open_short[-1])
                    self.fees.append(self.close_short[-1] * 0.01)

                else:
                    pass

            else:

                print('Error')
        
        # When candle is closed, append close price to data
        else:
            self.data.append(float(candle['c']))

        print(
            self.symbol, '| price: {} | c_min: {} // c_max: {} // pos: {} // net pnl: {} // fees: {}\n'.format(
                round(price, 2),
                round(c_min, 2),
                round(c_max, 2),
                self.position,
                round(sum(self.pnl) - sum(self.fees), 4),
                round(sum(self.fees), 4)
            )
        )
