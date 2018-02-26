"""Various Crypto Market APIs."""
import requests


class Market:
    """Market default class."""

    def get_name():
        """Get name of the current market."""
        return ""

    def get_products():
        """Get list of suported products."""
        return []

    def get_ticker(self, product):
        """Get ticker of the product."""

    def get_spot_price(self, product):
        """Get spot price of the product."""


class BitfinexMarket(Market):
    """Market Client for Bitfinex."""

    def get_ticker(self, product):
        """Get the current ticker.

        Args:
            product: The coin you want the ticker of.
        Returns:
            ticker: The ticker object.

        """
        if product == 'btc-usd':
            ticker = {}
            response = requests.get(
                'https://api.bitfinex.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError(
                    'GET https://api.bitfinex.com/v1/pubticker/btcusd {}'
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
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        if product == 'btc-usd':
            response = requests.get(
                'https://api.bitfinex.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError(
                    'GET https://api.bitfinex.com/v1/pubticker/btcusd {}'
                    .format(response.status_code))
            response = response.json()
            return response['last_price']


class CoinbaseMarket(Market):
    """Markert Client for Coinbase."""

    def __init__(self):
        """Initializer."""

    def get_name():
        """Get the name of the market."""
        return "Coinbase"

    def get_products(self):
        """Get list of supported markets."""
        return ['btc-usd', 'eth-usd', 'ltc-usd']

    def get_spot_price(self, product):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        if product in ['btc-usd', 'eth-usd', 'ltc-usd']:
            url = 'https://api.coinbase.com/v2/prices/' + product + '/spot'
            response = requests.get(url,
                                    data={'CB-VERSION': '2018-02-01'})
            if response.status_code != 200:
                raise RuntimeError('GET url {}'.format(response.status_code))
            response = response.json()
            return response['data']['amount']


class GdaxMarket(Market):
    """Market Client for GDAX."""

    def __init__(self):
        """Initializer."""

    def get_spot_price(self, product):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        if product == 'btc-usd':
            response = requests.get(
                'https://api.gdax.com/products/btc-usd/ticker')
            if response.status_code != 200:
                raise RuntimeError(
                    'GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['price']


class GeminiMarket(Market):
    """Market Client Gemini."""

    def __init__(self):
        """Initializer."""

    def get_spot_price(self, product):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        if product == 'btc-usd':
            response = requests.get(
                'https://api.gemini.com/v1/pubticker/btcusd')
            if response.status_code != 200:
                raise RuntimeError(
                    'GET https://api.coinbase.com/v2/prices/BTC-USD/spot {}'
                    .format(response.status_code))
            response = response.json()
            return response['last']
