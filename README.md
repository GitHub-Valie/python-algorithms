## Trading algorithms

### Algorithms

##### Basic algo

Using Numpy, generate an array of 500 floats between 0 and 1. For each float in the array, check if > or < 0.5

##### SMA algo

Price data for each timestamp is in a list of lists. Calculate a Standard Moving Average and compare its value to the closing price.

##### Crossover algo

The dataset is a csv file of OHLC data for BTCUSDT (Bitcoin)
Using Btalib, create two Standard Moving Averages with window sizes of 5 and 10. While keeping track of profit, position and order price, apply this trading strategy: Buy when the SMA_5 < SMA_10, Sell when SMA_10 < SMA_5. 

### Live algorithms

##### Basic live algo

Get historical data for BTCUSDT (Bitcoin). Using websocket protocol, create a websocket app which will process historical data and new data streamed live from Binance. Apply this trading strategy: 

* SMA_200 < Close: close long & go short
* SMA_200 > Close: close short & go long

##### Multi EMAs

Trying algorithms with multiple technical indicator parameters

##### Multi assets

Trying algorithms with a weighted portfolio of assets to trade

## Backtesting

Using backtrader, a backtesting package to backtest trading strategies and evaluate their performance

## Data analysis

Linear regression example and multivariate linear regression with pandas, sklearn, matplotlib and seaborn

* Linear regression

The dataset is a timeseries of ETHUSDT (Ethereum) price from Binance. The goal is to check if there is a linear relation between ETHUSDT minutely price and the number of trades made each minute.

* Multivariate linear regression

The datasets are timeseries of various cryptocurrencies. The goal is to check for interesting relations between cryptocurrencies.

## Datasets