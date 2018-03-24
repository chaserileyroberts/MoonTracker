"""Asset List."""
supported_assets = {
    "BTC": {
        "name": "Bitcoin",
        "markets": ["coinbase"]
    },
    "ETH": {
        "name": "Ethereum",
        "markets": ["coinbase"]
    },
    "LTC": {
        "name": "Litecoin",
        "markets": ["coinbase"]
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

assets = [(asset, supported_assets[asset]["name"])
          for asset in supported_assets]
