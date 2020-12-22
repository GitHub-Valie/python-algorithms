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
position = 0
pnl = 0
profit_counter = 0

# Define conditions
long_condition = True
short_condition = False

# Define lists
open_long = []
open_short = []
close_long = []
close_short = []

class Algorithm:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.data = deque([], maxlen=500)
        self.position = 0
        self.pnl = 0
        self.profit_counter = 0

        historical_data = futures_get_hist(
            symbol = symbol,
            interval = interval
        )

        for candle in historical_data:
            
            self.data.append(float(candle[4]))
            # print(self.data[-1])
    
    def get_ticks(self, candle):

        # print(close)

        # Implement strategy if candle is closed
        if candle['x'] == True:
            self.data.pop(0)
            self.data.append(float(candle['c']))
        
        # Implement strategy if candle is open
        else:
            self.data[-1] = float(candle['c'])
            # Dataframe transform
            df = pd.DataFrame(
                data = list(self.data),
                columns = ['close']
            )
            # Bollinger bands
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
            # print(df.iloc[-1])
            price = float(df['close'].iloc[-1])
            bb_high = float(df['bb_bbh'].iloc[-1])
            bb_low = float(df['bb_bbl'].iloc[-1])
            last_rsi = float(df['rsi'].iloc[-1])

            # Positions
            if self.position == 0:

                # Long condition is met
                if price < bb_low and last_rsi < 35:

                    print('GO LONG')
                    position = 1

                    open_long.append(price)

                # Short condition is met
                elif price > bb_high and last_rsi > 65:

                    print('GO SHORT')
                    position = -1

                    open_short.append(price)

                else:

                    pass

            elif self.position == 1:

                # Long condition no longer met
                if price > bb_low and rsi > 35:

                    print('CLOSE LONG')
                    position = 0

                    close_long.append(price)
                    
                    pnl.append(open_long[-1] - close_long[-1])
                    profit_counter += 1

                # Short condition is met
                elif price > bb_high and last_rsi > 65:

                    print('CLOSE LONG AND GO SHORT')
                    position = -1

                    close_long.append(price)
                    open_short.append(price)

                    pnl.append(open_long[-1] - close_long[-1])
                    profit_counter += 1

                else:

                    pass

            elif self.position == -1:

                # Short condition no longer met
                if price < bb_high and last_rsi < 65:

                    print('CLOSE SHORT')
                    position = 0

                    close_short.append(price)

                    pnl.append(close_short[-1] - open_short[-1])
                    profit_counter += 1

                # Long condition is met
                elif price < bb_low and last_rsi < 35:

                    print('CLOSE SHORT AND GO LONG')
                    position = 1

                    close_short.append(price)
                    open_long.append(price)

                    pnl.append(close_short[-1] - open_short[-1])
                    profit_counter += 1

                else:

                    pass

            else:

                print('Error')
        
        print(
            self.symbol, ': price: {} ; bb_h: {} ; bb_l: {} ; rsi: {}\nPnl: {}'.format(
                round(price, 1),
                round(bb_high, 1),
                round(bb_low, 1),
                round(last_rsi, 1),
                round(pnl, 1)
            )
        )
