import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']

# Loop through all csvs and create a data frame for each of them

def data(symbol):
    df = pd.read_csv(
        'data\{}.csv'.format(
            symbol
        ),
        dtype='float'   
    )

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

    return df

dfs = []

for symbol in symbols:
    dfs.append(data(symbol))

df = pd.concat(dfs, axis=1)

df.columns = pd.MultiIndex.from_product(
    [
        [
            symbol for symbol in symbols
        ],
        [
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Number of trades'
        ]
    ]
)


# Prepare data

btcusdt = df['BTCUSDT']
ethusdt = df['ETHUSDT']
xrpusdt = df['XRPUSDT']

btcusdt.columns = [
    'btcusdt_open',
    'btcusdt_high',
    'btcusdt_low',
    'btcusdt_close',
    'btcusdt_volume',
    'btcusdt_trades'
]

ethusdt.columns = [
    'ethusdt_open',
    'ethusdt_high',
    'ethusdt_low',
    'ethusdt_close',
    'ethusdt_volume',
    'ethusdt_trades'
]

xrpusdt.columns = [
    'xrpusdt_open',
    'xrpusdt_high',
    'xrpusdt_low',
    'xrpusdt_close',
    'xrpusdt_volume',
    'xrpusdt_trades'
]

df = pd.concat(
    [
        btcusdt['btcusdt_close'], 
        ethusdt['ethusdt_close'], 
        xrpusdt['xrpusdt_close'],
        btcusdt['btcusdt_volume'], 
        ethusdt['ethusdt_volume'], 
        xrpusdt['xrpusdt_volume'],
        btcusdt['btcusdt_trades'], 
        ethusdt['ethusdt_trades'], 
        xrpusdt['xrpusdt_trades']
    ],
    axis=1
)


# Data exploration

corr = df.corr() # Correlation

print(corr)

sns.heatmap(
    data=corr,
    annot=True,
    cmap='RdBu'
)
plt.show() # Visualize corr coefs
