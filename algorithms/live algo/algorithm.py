from portfolio import portfolio
import requests

# TODO: Add klines (request historical data)
# TODO: create function "next"

class Algorithm:
    def __init__(self, Asset, Weight):
        self.asset = Asset
        self.weight = Weight
