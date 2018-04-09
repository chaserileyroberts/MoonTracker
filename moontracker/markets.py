"""Various Crypto Market APIs."""
import requests
from datetime import datetime, timedelta


class Market:
    """Market default class."""

    def get_spot_price(self, product, time=datetime.utcnow()):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to the current time.
        Returns:
            price: The current price of the asset as a float.

        """
        raise NotImplementedError


    def get_percent_change(self, product, time):
        """Get the percent change of the asset over the specified time period.

        Args:
            product: The asset to get the percent change of.
            seconds: The time in seconds to get the change over.
        Returns:
            change: The percent change as a float.

        """
        current_price = get_spot_price(self, product)
        prev_price = get_spot_price(self, product, time - timedelta(seconds=time))
        return (current_price - prev_price) / prev_price


class BitfinexMarket(Market):
    """Market Client for Bitfinex."""

    def get_spot_price(self, product, time=datetime.utcnow()):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        product = product.upper()
        utc_time = int((time - datetime(1970, 1, 1)).total_seconds() * 1000)
        response = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:t{}USD/hist?limit=10&sort=1&start={}&end={}'.format(product, utc_time - 100000, utc_time))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.bitfinex.com/v2/candles/ {}'
                .format(response.status_code))
        response = response.json()
        return float(response[len(response) - 1][2])


class GdaxMarket(Market):
    """Market Client for GDAX."""

    def get_spot_price(self, product, time=datetime.utcnow()):
        """Get the coin price at the specified time.

        Args:
            product: The coin you want the value of.
            time: Time to get the price of the coin at, defaults to the current time.
        Returns:
            price: The price.

        """
        response = requests.get(
            'https://api.gdax.com/products/{}-usd/candles?start={}&end={}\
            &granularity=60'.format(product, time - timedelta(minutes=10), time))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.gdax.com/products/ {}'
                .format(response.status_code))
        response = response.json()
        return float(response[len(response)-1][4])


class GeminiMarket(Market):
    """Market Client Gemini."""

    def get_spot_price(self, product, time=datetime.utcnow()):
        """Get the current coin price.

        Args:
            product: The coin you want the value of.
        Returns:
            price: The current price.

        """
        utc_time = int((time - datetime(1970, 1, 1)).total_seconds()) - 120
        response = requests.get(
            'https://api.gemini.com/v1/trades/{}usd?since={}&limit_trades=1'.format(product, utc_time))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.gemini.com/v1/trades/{}'
                .format(response.status_code))
        response = response.json()
        return float(response[0]['price'])


class NasdaqMarket(Market):
    """Nasdeq Stock Market."""

    def get_spot_price(self, product, time=datetime.utcnow()):
        """Get stock price value from extrading."""
        date = time.date().strftime("%Y%m%d")
        response = requests.get(
            "https://api.iextrading.com/1.0/stock/{}/chart/date/{}".format(product, date))
        if response.status_code != 200:
            raise RuntimeError(
                'GET https://api.iextrading.com {}'
                .format(response.status_code))
        price = float(response.json()[12]['high'])
        return price


def lookupMarket(market):
    """Get market class from name string."""
    markets = {
        "bitfinex": BitfinexMarket,
        "gdax": GdaxMarket,
        "gemini": GeminiMarket,
        "nasdaq": NasdaqMarket,
        "coinbase": GdaxMarket
    }
    return markets[market]
