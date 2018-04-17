"""Price Tracker."""
from moontracker.markets import lookupMarket
from moontracker.assets import supported_assets


class PriceTracker():
    """Price tracking client. Works for stock and crypto."""

    def get_spot_price(self, asset, market=None):
        """Get the current price for the asset.

        Args:
            asset: The asset of the query.
            market: String of the market to pull from.
        Returns:
            price: float price of the asset.

        """
        if market is None:
            first_market = supported_assets[asset]["markets"][0]
            MarketClass = lookupMarket(first_market)
        elif market not in supported_assets[asset]["markets"]:
            raise NotImplementedError
        else:
            MarketClass = lookupMarket(market)
        mrkt = MarketClass()
        value = mrkt.get_spot_price(asset)
        return value

    def get_percent_change(self, asset, market=None, duration=3600):
        """Get the percent change for the asset.

        Args:
            asset: The asset of the query.
            market: String of the market to pull from.
            time: 
        Returns:
            change: float percent change of the asset over 'time' seconds.

        """
        if market is None:
            first_market = supported_assets[asset]["markets"][0]
            MarketClass = lookupMarket(first_market)
        elif market not in supported_assets[asset]["markets"]:
            raise NotImplementedError
        else:
            MarketClass = lookupMarket(market)
        mrkt = MarketClass()
        change = mrkt.get_percent_change(asset, duration)
        return change