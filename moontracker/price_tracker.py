"""Price Tracker."""
import requests
import json
from moontracker.markets import lookupMarket


class PriceTracker():
    """Price tracking client. Works for stock and crypto."""

    def __init__(self):
        """Initialize the client."""
        self.cryptos = set(['BTC', 'ETH', 'LTC'])

    def get_spot_price(self, asset, market=None):
        """Get the current price for the asset.

        Args:
            asset: The asset of the query.
            market: String of the market to pull from.
        Returns:
            price: float price of the asset.
        """
        # TODO(Chase): Possible attack here if we don't have full control
        # over what the value of asset is.
        if asset not in self.cryptos:
            # Get stock price value from extrading.
            response = requests.get(
                "https://api.iextrading.com/1.0/stock/" +
                asset +
                "/quote")
            price = float(json.loads(response.text)['latestPrice'])

        elif market is None:
            # Get the crypto currency value from coinbase.
            exchange = asset + "-USD"
            response = requests.get(
                'https://api.coinbase.com/v2/prices/' +
                exchange +
                '/spot/')
            price = float(json.loads(response.text)['data']['amount'])

        else:
            raise NotImplemented("Markets not yet supported.")
        return price
