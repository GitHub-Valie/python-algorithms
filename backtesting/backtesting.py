import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
from strategies import Basic_RSI, BuyAndHold_Target

start_cash = 10000

cerebro = bt.Cerebro()

df = pd.read_csv(
    'data\ETHUSDT.csv'
)

df.index = pd.to_datetime(
    df['Datetime'], 
    unit='s'
)

data = btfeeds.PandasData(dataname=df)

cerebro.adddata(data)

cerebro.broker.set_cash(start_cash)

cerebro.addstrategy(BuyAndHold_Target)

print(
    'Start:   $ {}'.format(
        round(cerebro.broker.get_value())
    )
)

cerebro.run()

print(
    'End:     $ {}'.format(
        round(cerebro.broker.getvalue())
    )
)