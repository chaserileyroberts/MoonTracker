"""Various Crypto Market APIs."""
import requests
from datetime import datetime, timedelta


class Market:
    """Market default class."""

    def _handle_request(self, request):
        """Helper function for get_spot_price.

        Args:
            request: The url for the request.
        Returns:
            response: The response as a JSON object.
        Raises:
            RuntimeErrror: If the request doesn't return a 200 status code.

        """
        response = requests.get(request)
        if response.status_code != 200:
            raise RuntimeError('GET {} {}'.format(request, response.status_code))
        return response.json()

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """
        raise NotImplementedError

    def get_percent_change(self, product, time):
        """Get the percent change of the asset over the specified time period.

        Args:
            product: The asset to get the percent change of.
            time: The time in seconds to get the change over.
        Returns:
            change: The percent change as a float.

        """
        current_price = self.get_spot_price(product)
        prev_price = self.get_spot_price(
            product, datetime.utcnow() - timedelta(seconds=time))
        return (current_price - prev_price) / prev_price


class BitfinexMarket(Market):
    """Market Client for Bitfinex."""

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """

        # Bitfinex requires the asset to be in upper case.
        product = product.upper()

        if time is None:
            request = 'https://api.bitfinex.com/v2/ticker/t{}USD'.format(product)

            response = self._handle_request(request)

            # Returns the latest trade price.
            return float(response[6])
        elif (datetime.utcnow() - time).total_seconds() > (31 * 24 * 60 * 60):
            raise ValueError("Time must be within 31 days of the current time.")
        else:
            # Bitfinex requires the time to be in milliseconds since epoch.
            start_time = int((time - datetime(1970, 1, 1)).total_seconds() * 1000)

            request = 'https://api.bitfinex.com/v2/candles/trade:1m:t{}USD/hist?limit=1&sort=1&start={}'.format(product, start_time)
        
            response = self._handle_request(request)

            # If there are no trades after the start time, just get the last
            # trade that ever occurred for the asset.
            if len(response) == 0:
                return self.get_spot_price(product)

            # Return the first trade in the returned history.
            # 0 returns the first timeframe.
            # 2 returns the price of the last trade  in the timeframe.
            return float(response[0][2])


class CoinbaseMarket(Market):
    """Market Client for Coinbase."""

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """

        if time is None:
            request = 'https://api.coinbase.com/v2/prices/{}-usd/spot'.format(product)
        elif (datetime.utcnow() - time).total_seconds() > (31 * 24 * 60 * 60):
            raise ValueError("Time must be within 31 days of the current time.")
        else:
            # Coinbase only allows historical prices by date.
            date = time.date().isoformat()
            request = 'https://api.coinbase.com/v2/prices/{}-usd/spot?date={}'.format(product, date)
        response = self._handle_request(request)

        return float(response['data']['amount'])


class GdaxMarket(Market):
    """Market Client for GDAX."""

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """
            
        if time is None:
            request = 'https://api.gdax.com/products/{}-usd/ticker'.format(product)
            response = self._handle_request(request)
            return float(response['price'])
        elif (datetime.utcnow() - time).total_seconds() > (31 * 24 * 60 * 60):
            raise ValueError("Time must be within 31 days of the current time.")
        else:
            # The start time is arbitrarily 10 minutes behind the end time.
            start_time = time - timedelta(minutes=10)

            request = 'https://api.gdax.com/products/{}-usd/candles?start={}&end={}&granularity=60'.format(product, start_time, time)
            response = self._handle_request(request)

            # If there are no trades after the start time, just get the last
            # trade that ever occurred for the asset.
            if len(response) == 0:
                return self.get_spot_price(product)


            # Return the latest bucket's closing trade.
            # len(response)-1 returns the latest bucket.
            # 4 returns the closing trade's price in the bucket.
            return float(response[len(response) - 1][4])


class GeminiMarket(Market):
    """Market Client Gemini."""

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """

        if time is None:
            request = 'https://api.gemini.com/v1/pubticker/{}usd'.format(product)
            response = self._handle_request(request)
            return float(response['last'])
        elif (datetime.utcnow() - time).total_seconds() > (7 * 24 * 60 * 60):
            raise ValueError("Time must be within 7 days of the current time.")
        else:
            # Gemini requires the time to be in seconds since epoch.
            # Arbitrarily 10 minutes behind the target time.
            start_time = int((time - datetime(1970, 1, 1)).total_seconds()) - 600

            request = 'https://api.gemini.com/v1/trades/{}usd?since={}&limit_trades=100'.format(product, start_time)
            response = self._handle_request(request)

            # If there are no trades after the start time, just get the last
            # trade that ever occurred for the asset.
            if len(response) == 0:
                return self.get_spot_price(product)

            # Return the latest trade.
            # len(response)-1 returns the latest trade.
            # 'price' returns the price of the trade.
            return float(response[len(response) - 1]['price'])


class NasdaqMarket(Market):
    """Nasdaq Stock Market."""

    def get_spot_price(self, product, time=None):
        """Get the asset price at the specified time.

        Args:
            product: The asset you want the price of.
            time: The time to get the price for, defaults to None.
                  When time is None, gets the price of the latest trade.
        Returns:
            price: The current price of the asset as a float.
        Raises:
            RuntimeError: If the request doesn't return a 200 status code.
            ValueError: If the time is not supported by the API.

        """

        if time is None:
            request = "https://api.iextrading.com/1.0/stock/{}/quote".format(product)
            response = self._handle_request(request)
            return float(response['latestPrice'])
        elif (datetime.utcnow() - time).total_seconds() > (7 * 24 * 60 * 60):
            raise ValueError("Time must be within 7 days of the current time.")
        else:
            date = time.date().strftime("%Y%m%d")

            request = "https://api.iextrading.com/1.0/stock/{}/chart/date/{}".format(product, date)
            response = self._handle_request(request)

            # If there are no trades after the start time, just get the last
            # trade that ever occurred for the asset.
            if len(response) == 0:
                return self.get_spot_price(product)

            # Return the latest trade price.
            # len(response)-1 returns the latest timeframe.
            # 'average' returns the average price of the timeframe.
            return float(response[len(response) - 1]['average'])


def lookupMarket(market):
    """Get market class from name string."""
    markets = {
        "bitfinex": BitfinexMarket,
        "gdax": GdaxMarket,
        "gemini": GeminiMarket,
        "nasdaq": NasdaqMarket,
        "coinbase": CoinbaseMarket
    }
    return markets[market]
