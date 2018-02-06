import requests
import time

class Market:
    def get_ticker(self, product):
        pass

    def get_spot_price(self, product):
        pass

class BitfinexMarket(Market):
    def get_ticker(self, product):
        if product == 'btc-usd':
            ticker = {}
            response = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError('GET https://api.bitfinex.com/v1/pubticker/btcusd {}'
                    .format(response.status_code))
            response = response.json()
            ticker['bid'] = response['bid']
            ticker['ask'] = response['ask']
            ticker['price'] = response['last_price']
            ticker['low'] = response['low']
            ticker['high'] = response['high']
            ticker['volume'] = response['volume']
            return ticker

    def get_spot_price(self, product):
        if product == 'btc-usd':
            response = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError('GET https://api.bitfinex.com/v1/pubticker/btcusd {}'
                    .format(response.status_code))
            response = response.json()
            return response['last_price']

class CoinbaseMarket(Market):
    def __init__(self):
        pass

    def get_spot_price(self, product):
        if product == 'btc-usd':
            response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot',
                data={'CB-VERSION': '2018-02-01'})
            if response.status_code != 200:
                raise RuntimeError('GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['data']['amount']

class GdaxMarket(Market):
    def __init__(self):
        pass

    def get_spot_price(self, product):
        if product == 'btc-usd':
            response = requests.get('https://api.gdax.com/products/btc-usd/ticker')
            if response.status_code != 200:
                raise RuntimeError('GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['price']

class GeminiMarket(Market):
    def __init__(self):
        pass

    def get_spot_price(self, product):
        if product == 'btc-usd':
            response = requests.get('https://api.gemini.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError('GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['last']



