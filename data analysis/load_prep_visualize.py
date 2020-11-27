# This program loads a csv file, prepares the data and plots it
# for visualization

import pandas
import matplotlib.pyplot as plt

symbol = 'XRPUSDT'

# Loading csv in dataframe and assign column names
df = pandas.read_csv(
    'data\{}.csv'.format(symbol)
)

# Index creation
df.index = pandas.to_datetime(
    df['Datetime'], 
    unit='s'
)

# Cleaning dataframe
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

print(df.head())

# Data visualization
df.plot(y=['Close'])
plt.title(symbol)
plt.show()
