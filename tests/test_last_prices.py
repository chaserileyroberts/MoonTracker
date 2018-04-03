from datetime import datetime
import time
import json

from moontracker.models import LastPrice

from moontracker.last_prices import get_last_prices_json


def test_get_last_prices_json():
    last_prices = [
        LastPrice(symbol='BTC', price='1000.5',
                  timestamp=datetime.utcfromtimestamp(1000001)),
        LastPrice(symbol='LTC', price='201.5',
                  timestamp=datetime.utcfromtimestamp(1000002))
    ]
    last_prices_json = get_last_prices_json(last_prices)
    last_prices2 = json.loads(last_prices_json)
    assert(len(last_prices) == len(last_prices2))
    for i in range(len(last_prices)):
        lp1 = last_prices[i]
        lp2 = last_prices2[i]
        assert(len(lp2) == 3)
        assert(lp1.symbol == lp2['symbol'])
        assert(lp1.price == lp2['price'])
        assert(lp2['timestamp'] == time.mktime(lp1.timestamp.timetuple()))
