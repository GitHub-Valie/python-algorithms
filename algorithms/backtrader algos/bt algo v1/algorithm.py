# Imports
from collections import deque
from portfolio import portfolio
from functions import futures_get_hist
from pprint import pprint
import pandas as pd

# Implement technical analysis
from ta.utils import dropna
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

# Define position, pnl and pnl_counter

# Define conditions
long_condition = True
short_condition = False

# Define lists

class Algorithm:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.data = deque([], maxlen=500)
        self.tmp = deque([], maxlen=500)
        self.position = 0
        self.pnl = []
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

        
        # When candle is open, append all data from self.data in tmp list and append tick data candle['c'] to tmp
        if candle['x'] == False:
            for close in list(self.data):
                self.tmp.append(close)
            self.tmp.append(float(candle['c']))

            df = pd.DataFrame(
                data = list(self.tmp),
                columns = ['close']
            )

            # Bollinger Bands
            indicator_bb = BollingerBands(
                close=df['close'],
                window=20,
                window_dev=2
            )

            # Relative Strength Index
            indicator_rsi = RSIIndicator(
                close=df['close'],
                window=14,
                fillna=False
            )

            df['bb_bbh'] = indicator_bb.bollinger_hband()
            df['bb_bbl'] = indicator_bb.bollinger_lband()
            df['rsi'] = indicator_rsi.rsi()

            price = float(df['close'].iloc[-1])
            bb_high = float(df['bb_bbh'].iloc[-1])
            bb_low = float(df['bb_bbl'].iloc[-1])
            last_rsi = float(df['rsi'].iloc[-1])

            # Positions

            if self.position == 0:

                # Long condition is met
                if price < bb_low or last_rsi < 30:
                    print('GO LONG')
                    self.position = 1
                    self.open_long.append(price)

                # Short condition is met
                elif price > bb_high or last_rsi > 70:
                    print('GO SHORT')
                    self.position = -1
                    self.open_short.append(price)

                else:
                    pass

            elif self.position == 1:

                # Short condition is met
                if price > bb_high or last_rsi > 70:
                    print('CLOSE LONG AND GO SHORT')
                    self.position = -1
                    self.close_long.append(price)
                    self.open_short.append(price)
                    self.pnl.append(open_long[-1] - close_long[-1])
                    self.profit_counter += 1

                else:
                    pass

            elif self.position == -1:

                # Long condition is met
                if price < bb_low or last_rsi < 30:
                    print('CLOSE SHORT AND GO LONG')
                    self.position = 1
                    self.close_short.append(price)
                    self.open_long.append(price)
                    self.pnl.append(close_short[-1] - open_short[-1])
                    self.profit_counter += 1

                else:
                    pass

            else:

                print('Error')
        
        # When candle is closed, append close price to data
        else:
            # print('candle is closed')
            self.data.append(float(candle['c']))

        print(
            self.symbol, ': price: {} ; bb_h: {} ; bb_l: {} ; rsi: {}\nPosition: {} ; Pnls: {}'.format(
                round(price, 1),
                round(bb_high, 1),
                round(bb_low, 1),
                round(last_rsi, 1),
                self.position,
                round(sum(self.pnl), 4)
            )
        )
