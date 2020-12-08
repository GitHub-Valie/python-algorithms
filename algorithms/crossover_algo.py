import pandas as pd
import btalib
import numpy as np

symbol = 'BTCUSDT'

# Import data from csv file
df = pd.read_csv(
    'data\{}.csv'.format(
        symbol
    )
)

# Data preparation
df.index = pd.to_datetime(
    df['Datetime'], 
    unit='s'
)

df = df.drop(
    columns = [
        'Datetime',
        'Close time',
        'Quote asset volume', 
        'Taker BUY base asset volume', 
        'Taker BUY quote asset volume', 
        'Ignore'
    ]
)

# SMA indicators
df['sma_5'] = btalib.sma(
    df.Close,
    period = 5
).df

df['sma_10'] = btalib.sma(
    df.Close,
    period = 10
).df

# arr = df['sma_10'].to_numpy()
# print(arr)

# print(df['sma_10_numpy'], df['sma_10'])
# print('Types :', type(df['sma_10_numpy']), type(df['sma_10']))

df = df.iloc[10:]

n = 0

# Strategy: If sma-5 CROSSES OVER sma-10: Buy / vice-versa

position = 0 # Add position tracker (0 or 1), default = 0
profit_counter = 0 # Add profit counter
orders = [] # Add order price-tracking
pnl = [] # Add PnL calculation

while n < len(df):

    buy_sell = False
    
    if position == 0 and df.iloc[n, 6] > df.iloc[n, 7]:
        print(
            df.index[n],
            'BUY    | sma_5: {} | sma_10: {} | Price: {}'.format(
                round(
                    df.iloc[n, 6]
                ),
                round(
                    df.iloc[n, 7]
                ),
                df.iloc[n, 3]
            )
        )
        position = 1
        orders.append(df.iloc[n, 3])
        buy_sell = False
    
    elif position == 1 and df.iloc[n, 6] < df.iloc[n, 7]:
        print(
            df.index[n],
            'SELL   | sma_5: {} | sma_10: {} | Price: {}'.format(
                round(
                    df.iloc[n, 6]
                ),
                round(
                    df.iloc[n, 7]
                ),
                df.iloc[n, 3]
            )
        )
        position = 0
        orders.append(df.iloc[n, 3])
        buy_sell = True

        profit = orders[-2] - orders[-1] # order[-1] is sell price, order[-2] is buy price
        pnl.append(profit)

        if profit > 0:
            profit_counter += 1

    else:
        pass
    
    n += 1

# Summary
print('Orders passed:   ', len(orders))
print('Profit counter:  ', profit_counter)
print(
    'Win Rate:   ',
    round(
        profit_counter / len(orders) * 100, 2
    ),
    '%'
)
print(
    'PnL:       {}'.format('$'), 
    round(sum(pnl), 2)
)
