from moontracker.price_tracker import PriceTracker
import pytest


def test_btc():
    pt = PriceTracker()
    price = pt.get_spot_price("BTC")
    assert isinstance(price, float)


def test_ltc():
    pt = PriceTracker()
    price = pt.get_spot_price("LTC")
    assert isinstance(price, float)


def test_eth():
    pt = PriceTracker()
    price = pt.get_spot_price("ETH")
    assert isinstance(price, float)


def test_aapl():
    pt = PriceTracker()
    price = pt.get_spot_price("AAPL")
    assert isinstance(price, float)


def test_googl():
    pt = PriceTracker()
    price = pt.get_spot_price("GOOGL")
    assert isinstance(price, float)


def test_not_implemented_error():
    pt = PriceTracker()

    with pytest.raises(NotImplementedError) as err:
        pt.get_spot_price("BTC", "FAKE")

    with pytest.raises(NotImplementedError) as err:
        pt.get_percent_change("BTC", "FAKE")
