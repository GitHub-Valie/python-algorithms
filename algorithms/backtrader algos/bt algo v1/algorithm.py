# Imports
from collections import deque
from portfolio import portfolio
from functions import futures_get_hist
from pprint import pprint

# Implement Backtrader strategy
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd

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
    
    def next(self, close):

        # print(close)

        if close['x'] == True:
            self.data.pop(0)
            self.data.append(float(close['c']))
        
        else:
            self.data[-1] = float(close['c'])

        print(self.data[-1])



    # # Positions
    # if position == 0:

    #     # Long condition is met
    #     if long_condition == True:

    #         print('GO LONG')
    #         position = 1

    #         open_long.append(price)

    #     # Short condition is met
    #     elif short_condtion == True:

    #         print('GO SHORT')
    #         position = -1

    #         open_short.append(price)

    #     else:

    #         pass

    # elif position == 1:

    #     # Long condition no longer met
    #     if long_condition == False:

    #         print('CLOSE LONG')
    #         position = 0

    #         close_long.append(price)
            
    #         pnl.append(open_long[-1] - close_long[-1])
    #         profit_counter += 1

    #     # Short condition is met
    #     elif short_condition == True:

    #         print('CLOSE LONG AND GO SHORT')
    #         position = -1

    #         close_long.append(price)
    #         open_short.append(price)

    #         pnl.append(open_long[-1] - close_long[-1])
    #         profit_counter += 1

    #     else:

    #         pass

    # elif position == -1:

    #     # Short condition no longer met
    #     if short_condition == False:

    #         print('CLOSE SHORT')
    #         position = 0

    #         close_short.append(price)

    #         pnl.append(close_short[-1] - open_short[-1])
    #         profit_counter += 1

    #     # Long condition is met
    #     elif long_condtion == True:

    #         print('CLOSE SHORT AND GO LONG')
    #         position = 1

    #         close_short.append(price)
    #         open_long.append(price)

    #         pnl.append(close_short[-1] - open_short[-1])
    #         profit_counter += 1

    #     else:

    #         pass

    # else:

    #     print('Error')
