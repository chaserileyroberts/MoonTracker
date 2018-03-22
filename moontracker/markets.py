"""Various Crypto Market APIs."""
import requests


class Market:
    """Market default class."""

    def get_products():
        """Get list of suported products."""
        return []

    def get_spot_price(self, product):
        """Get spot price of the product."""


class BitfinexMarket(Market):
    """Market Client for Bitfinex."""

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
            return float(response['last_price'])


class CoinbaseMarket(Market):
    """Markert Client for Coinbase."""

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
            return float(response['data']['amount'])


class GdaxMarket(Market):
    """Market Client for GDAX."""

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
            return float(response['price'])


class GeminiMarket(Market):
    """Market Client Gemini."""

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
            return float(response['last'])


def lookupMarket(market):
    markets = {
        "bitfinex": BitfinexMarket,
        "coinbase": CoinbaseMarket,
        "gdax": GdaxMarket,
        "gemini": GeminiMarket
    }
    return markets[market]
