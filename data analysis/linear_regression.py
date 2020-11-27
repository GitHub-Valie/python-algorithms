import pandas
import numpy
from sklearn.linear_model import LinearRegression

symbol = 'ETHUSDT'

df = pandas.read_csv(
    'data\{}.csv'.format(symbol)
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

X, y = df['Number of trades'], df['Close']

X, y = X.values, y.values
X, y = X.reshape((-1, 1)), numpy.array(y)

model = LinearRegression()

model.fit(X, y)

model = LinearRegression().fit(X, y)

r_square = model.score(X, y)
intercept = model.intercept_
slope = model.coef_

print('R-square: ', str(r_square))
print('Intercept: ', str(intercept))
print('Slope: ', str(slope))