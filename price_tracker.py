"""Price Tracker."""
import requests
import json


class PriceTracker():
    """Price tracking client. Works for stock and crypto."""

    def __init__(self):
        """Initialize the client."""
        self.cryptos = set(['BTC', 'ETH', 'LTC'])

    def get_spot_price(self, asset):
        """Get the current price for the asset.

        Args:
            asset: The asset of the query.
        """
        # TODO(Chase): Possible attack here if we don't have full control
        # over what the value of asset is.
        if asset in self.cryptos:
            # Get the crypto currency value from coinbase.
            exchange = asset + "-USD"
            response = requests.get(
                'https://api.coinbase.com/v2/prices/' +
                exchange +
                '/spot/')
            price = float(json.loads(response.text)['data']['amount'])

        else:
            # Get stock price value from extrading.
            response = requests.get(
                "https://api.iextrading.com/1.0/stock/" +
                asset +
                "/quote")
            price = json.loads(response.text)['latestPrice']
        return price
