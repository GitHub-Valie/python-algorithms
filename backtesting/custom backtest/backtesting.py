# Pseudo code

# Import data from "data" folder
import json
from pprint import pprint
from datetime import datetime
import pandas as pd
from ta.trend import EMAIndicator
import matplotlib.pyplot as plt

# Load json file
with open('data\BTCUSDT_1m_future.json') as json_file:
    data = json.load(json_file)
    # pprint(data[-10:]) # Explore data
    # pprint(data[:10])

print(
    'Start date: ', datetime.fromtimestamp(
        float(data[0][0]) / 1000
    ),
    '\nEnd date: ', datetime.fromtimestamp(
        float(data[-1][0]) / 1000
    ),
    '\nLength: ', len(data)
)

# Process json file
closes = []
for candle in data:
    closes.append(float(candle[4]))

print(
    'Max: ', max(closes),
    '\nMin: ', min(closes)
)

df = pd.DataFrame(
    data = closes,
    columns = ['close']
)

# Build technical indicators
emas_Used = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

for x in emas_Used:
    ema = x
    indicator_ema = EMAIndicator(
        close=df['close'],
        window=x,
        fillna=False
    )
    df['ema_' + str(ema)] = indicator_ema.ema_indicator()
# print(df.tail())

# Strategy
position = 0
open_long = []
open_short = []
close_long = []
close_short = []
pnl = []
fees = []

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
    price = df['close'][i]

    if position == 0:

        # Entry point when short term emas > long term emas
        if c_min > c_max:
            print(i, ': GO LONG')
            position = 1
            open_long.append(price)

        # Short condition is met
        elif c_max > c_min:
            print(i, ': GO SHORT')
            position = -1
            open_short.append(price)

        else:
            pass

    elif position == 1:

        # Short condition is met
        if c_max > c_min:
            print(i, ': CLOSE LONG AND GO SHORT')
            position = -1
            close_long.append(price)
            open_short.append(price)
            fees.append(close_long[-1] * 0.01)
            pnl.append(open_long[-1] - close_long[-1])

        else:
            pass

    elif position == -1:

        # Long condition is met
        if c_min > c_max:
            print(i, ': CLOSE SHORT AND GO LONG')
            position = 1
            close_short.append(price)
            open_long.append(price)
            pnl.append(close_short[-1] - open_short[-1])
            fees.append(close_short[-1] * 0.01)

        else:
            pass

    else:
        print('Error')

print(
    'net pnl: {} \nfees: {}'.format(
        round(sum(pnl) - sum(fees), 4),
        round(sum(fees), 4)
    )
)

# Visualize data (last 24 hours)
# df.iloc[-1440:].plot(
#     color = [
#         '#1ab1cd',
#         '#6fff00',
#         '#7cff00',
#         '#a3ff00',
#         '#d6ff00',
#         '#f0ff00',
#         '#ffdb00',
#         '#ffb400',
#         '#ff9a00',
#         '#ff6700',
#         '#ff4000',
#         '#ff2700',
#         '#ff0000'
#     ]
# )
# plt.show()
