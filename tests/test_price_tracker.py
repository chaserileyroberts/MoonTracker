from price_tracker import PriceTracker


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
