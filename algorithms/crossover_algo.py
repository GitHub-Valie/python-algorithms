import pandas as pd
import btalib

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

df = df.iloc[10:]

# Strategy1: if sma_5 is over sma_10: BUY
# if sma_5 is under sma_10: SELL

n = 0

while n < len(df):
    if df.iloc[n, 6] > df.iloc[n, 7]: # if sma_5 > sma_10
        print(
            df.index[n],
            ': FAST > SLOW / BUY! ', 
            round(df.iloc[n, 6]), 
            ' > ', 
            round(df.iloc[n, 7])
        )
    else: # sma_5 < sma_10
        print(
            df.index[n],
            ': FAST < SLOW / SELL! ',
            round(df.iloc[n, 6]),
            ' < ',
            round(df.iloc[n, 7])
        )
    
    n = n + 1

# TODO: Strategy 2: If sma-5 CROSSES OVER sma-10: Buy / vice-versa