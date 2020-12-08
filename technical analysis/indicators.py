# TODO: Request data from binance servers and create a standard moving average using numpy

import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

from data import closes

a = np.array(closes)

# Simple Moving Average with a rolling window of 'w'
def sma(arr, window):
    return np.convolve(arr, np.ones(window), 'valid') / window

# Exponential Weighted Moving Average
def ewma(arr, alpha, window):
    '''
    :arr: array
    :param alpha: specify decay [0, 1]
    :window: length of ewma
    '''
    arr = arr[-(len(arr) - window + 1):] # Re-adjusting length of arr so it has the same len as sma
    ewma_arr = np.zeros_like(arr) # returns an array of zeros the same length as arr
    ewma_arr[0] = arr[0] # first value in list ewma_arr is equal to first value in list arr
    for t in range(1, arr.shape[0]):
        ewma_arr[t] = alpha * arr[t] + (1 - alpha) * ewma_arr[t - 1]
    
    return ewma_arr

sma = sma(
    arr=a,
    window=20
)

ewma = ewma(
    arr=a,
    alpha=0.33,
    window=20
)

a = a[-481:]

fig, ax = plt.subplots()

ax.plot(a, label='BTCUSDT close')
ax.plot(sma, label='sma 20 periods')
ax.plot(ewma, label='ewma 20 periods')
leg = ax.legend()

plt.show()