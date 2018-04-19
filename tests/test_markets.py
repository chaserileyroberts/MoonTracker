from moontracker.markets import (Market, CoinbaseMarket, NasdaqMarket,
                                 GdaxMarket, GeminiMarket, lookupMarket)
import pytest
from datetime import datetime, timedelta


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


def test_not_implemented_error():
    market = Market()

    with pytest.raises(NotImplementedError) as err:
        market.get_spot_price('BTC')


def test_runtime_error():
    market = Market()

    with pytest.raises(RuntimeError) as err:
        market._handle_request('https://api.gdax.com/products/FAKE')


def test_value_errors():
    markets = [CoinbaseMarket, GdaxMarket, GeminiMarket, NasdaqMarket]
    for m in markets:
        mrkt = m()
        with pytest.raises(ValueError) as err:
            mrkt.get_spot_price('BTC', datetime.utcnow() - timedelta(days=40))
