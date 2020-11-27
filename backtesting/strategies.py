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

class BuyAndHold_Target(bt.Strategy):
    def start(self):
        self.val_start = self.broker.get_cash()  # Starting cash

    def nextstart(self):
        # Buy with all the available cash
        size = int(self.broker.get_cash() / self.data)
        self.buy(size=size)

    def stop(self):
        # Calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))
