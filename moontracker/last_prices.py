"""Last Price getter."""
import json
import time

from moontracker.extensions import socketio
from moontracker.models import LastPrice


@socketio.on('connect', namespace='/lastpriceslive')
def last_prices(broadcast=False):
    """Send the last price to the client."""
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
                  namespace='/lastpriceslive', broadcast=broadcast)


def broadcast_last_prices():
    """Send the last price to all the clients."""
    last_prices(broadcast=True)
