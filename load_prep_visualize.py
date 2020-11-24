# This program loads a csv file, prepares the data and plots it
# for visualization

import pandas
import matplotlib.pyplot as plt

# Loading csv in dataframe and assign column names
df = pandas.read_csv(
    'data\BTCUSDT.csv', 
    names = [
        'Open time', 
        'Open', 
        'High', 
        'Low', 
        'Close', 
        'Volume', 
        'Close time', 
        'Quote asset volume', 
        'Number of trades', 
        'Taker BUY base asset volume', 
        'Taker BUY quote asset volume', 
        'Ignore'
    ]
)

# Index creation
df.index = pandas.to_datetime(
    df['Open time'], 
    unit='s'
)

# Cleaning dataframe
df = df.drop(
    columns = [
        'Open time',
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
plt.show()
