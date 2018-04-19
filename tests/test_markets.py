from moontracker.markets import (Market,
                                 GdaxMarket, GeminiMarket, lookupMarket)


def test_all_markets_sanity():
    markets = [GdaxMarket, GeminiMarket]
    for m in markets:
        mrkt = m()
        value = mrkt.get_spot_price('BTC')
        assert isinstance(value, float)


def test_lookupMarket():
    markets = ['coinbase', 'gdax', 'gemini', 'nasdaq']
    for m in markets:
        mrkt = lookupMarket(m)
        assert issubclass(mrkt, Market)
