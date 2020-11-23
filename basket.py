# TODO: Create a basket of technical indicators

from pprint import pprint

# The main idea is to create one indicator which will serve as a signal
# and use a complementary indicator that provides a confirmation

trend_indicators = [
    "ADX", "MA", "MACD", "Parabolic SAR"
]

momentum_indicators = [
    "CCI", "RSI", "Stochastic"
]

volatility_indicators = [
    "ATR", "BB", "Std. Dev"
]

volume_indicators = [
    "Chaikin Oscillator",
    "On Balance Volume",
    "Rate of Change"
]

indicator_types = {
    'trend_indicators' : trend_indicators,
    'momentum_indicators' : momentum_indicators,
    'volatility_indicators' : volatility_indicators,
    'volume_indicators' : volume_indicators
}

pprint(indicator_types)

