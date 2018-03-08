import json
import time

from moontracker.extensions import socketio
from moontracker.models import LastPrice


def broadcast_last_prices():
    last_prices = LastPrice.query.all()
    last_prices_obj = [
        {
            'symbol': last_price.symbol,
            'price': last_price.price,
            'timestamp': time.mktime(last_price.timestamp.timetuple()),
        }
        for last_price in last_prices
    ]
    socketio.emit('json', json.dumps(last_prices_obj),
                  namespace='/lastpriceslive', broadcast=True)
