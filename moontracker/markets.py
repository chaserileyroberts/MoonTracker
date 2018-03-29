"""Various Crypto Market APIs."""
import requests


class Market:
    """Market default class."""

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
        response = requests.get(
            'https://api.bitfinex.com/v1/pubticker/{}usd'.format(product))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.bitfinex.com/v1/pubticker/btcusd {}'
                .format(response.status_code))
        response = response.json()
        return float(response['last_price'])


class CoinbaseMarket(Market):
    """Markert Client for Coinbase."""

    def get_spot_price(self, product):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        url = 'https://api.coinbase.com/v2/prices/{}-usd/spot'.format(product)
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
        response = requests.get(
            'https://api.gdax.com/products/{}-usd/ticker'.format(product))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.gdax.com/products/ {}'
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
        response = requests.get(
            'https://api.gemini.com/v1/pubticker/{}usd'.format(product))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.gemini.com/v1/pubticker/{}'
                .format(response.status_code))
        response = response.json()
        return float(response['last'])


class NasdeqMarket(Market):
    """Nasdeq Stock Market."""

    def get_spot_price(self, product):
        """Get stock price value from extrading."""
        response = requests.get(
            "https://api.iextrading.com/1.0/stock/" +
            product +
            "/quote")
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.iextrading.com {}'
                .format(response.status_code))
        price = float(response.json()['latestPrice'])
        return price


def lookupMarket(market):
    """Get market class from name string."""
    markets = {
        "bitfinex": BitfinexMarket,
        "coinbase": CoinbaseMarket,
        "gdax": GdaxMarket,
        "gemini": GeminiMarket,
        "nasdeq": NasdeqMarket
    }
    return markets[market]
