from moontracker.markets import (Market, BitfinexMarket, CoinbaseMarket,
                                 GdaxMarket, GeminiMarket, lookupMarket)


def test_all_markets():
    markets = [BitfinexMarket, CoinbaseMarket, GdaxMarket, GeminiMarket]
    for m in markets:
        mrkt = m()
        value = mrkt.get_spot_price('btc-usd')
        assert isinstance(value, float)


def test_lookupMarket():
    markets = ['bitfinex', 'coinbase', 'gdax', 'gemini']
    for m in markets:
        mrkt = lookupMarket(m)
        assert issubclass(mrkt, Market)
