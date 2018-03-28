"""Asset List."""
supported_assets = {
    "BTC": {
        "name": "Bitcoin",
        "markets": ["coinbase", "gemini", "bitfinex", "gdax"]
    },
    "ETH": {
        "name": "Ethereum",
        "markets": ["coinbase", "gemini", "bitfinex", "gdax"]
    },
    "LTC": {
        "name": "Litecoin",
        "markets": ["coinbase", "bitfinex", "gdax"]
    },
    "GOOGL": {
        "name": "Google",
        "markets": ["nasdeq"]
    },
    "AAPL": {
        "name": "Apple",
        "markets": ["nasdeq"]
    },
    "FB": {
        "name": "Facebook",
        "markets": ["nasdeq"]
    },
}

assets = sorted([(asset, supported_assets[asset]["name"])
          for asset in supported_assets])

market_apis = set()
for m in supported_assets:
    market_apis |= set(supported_assets[m]["markets"])

market_apis = sorted(list(market_apis))
