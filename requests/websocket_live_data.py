import websocket, json
from pprint import pprint

# {'E': 1606836912299,
#  'e': 'kline',
#  'k': {'B': '0', # Ignore
#        'L': 492877013, # Last trade ID
#        'Q': '183517.51285545', # taker buy quote asset volume
#        'T': 1606836959999, # kline close time
#        'V': '9.52020400', # taker buy base asset volume
#        'c': '19271.43000000', # Close price
#        'f': 492876581, # First trade ID
#        'h': '19286.66000000', # High price
#        'i': '1m', # Interval
#        'l': '19265.08000000', # Low price
#        'n': 433, # Number of trades
#        'o': '19282.22000000', # Open price
#        'q': '522736.43603941', # Quote asset volume
#        's': 'BTCUSDT', # Symbol
#        't': 1606836900000, # kline start time
#        'v': '27.11860100', # Base asset volume
#        'x': False}, # Is candle closed?
#  's': 'BTCUSDT'}

BASE_URL = "wss://stream.binance.com:9443"
SYMBOL = "BTCUSDT"
ENDPOINT = "/ws/{}@kline_1m".format(SYMBOL.lower())

def on_open(ws):
    print("Opened connection")

def on_close(ws):
    print("Closed connection")

def on_message(ws, message):
    json_message = json.loads(message)
    # pprint(json_message)
    candle = json_message['k']
    pprint(candle)

while True:
    ws = websocket.WebSocketApp(
        BASE_URL + ENDPOINT,
        on_open=on_open,
        on_close=on_close,
        on_message=on_message
    )
    ws.run_forever()