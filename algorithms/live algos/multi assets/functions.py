import requests, json

def futures_get_hist(symbol, interval):
    '''
    Get historical klines for a futures pair    
    :symbol: str, i.e "BTCUSDT"     
    :interval: str, i.e "1m"    
    '''
    r = requests.get(
        "https://fapi.binance.com" + "/fapi/v1/klines",
        params = {
            'symbol': symbol,
            'interval': interval
        }
    )

    req = r.json()
    return req