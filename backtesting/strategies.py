import backtrader as bt
import backtrader.feeds as btfeeds
from backtrader.indicators import RSI_SMA

class Basic_RSI(bt.Strategy):

    def __init__(self):
        self.rsi = RSI_SMA(
            self.data.close,
            period = 21
        )

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=10)

        else:
            if self.rsi > 70:
                self.sell(size=10)