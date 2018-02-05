import requests

class Market:
    def get_spot_price(self, product, currency):
        pass

class CoinbaseMarket(Market):
    def __init__(self):
        pass

    def get_spot_price(self, product, currency):
        product = product.lower()
        currency = currency.lower()
        if product == 'btc' and currency == 'usd':
            response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot',
                data={'CB-VERSION': '2018-02-01'})
            if response.status_code != 200:
                raise RuntimeError('GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['data']['amount']



