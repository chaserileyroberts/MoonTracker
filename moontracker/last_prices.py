"""Last Price getter."""
import json
import time

from moontracker.extensions import socketio
from moontracker.models import LastPrice


def get_last_prices_json(last_prices):
    """Create json for last prices."""
    last_prices_obj = [
        {
            'symbol': last_price.symbol,
            'price': last_price.price,
            'timestamp': time.mktime(last_price.timestamp.timetuple()),
        }
        for last_price in last_prices
    ]
    return json.dumps(last_prices_obj)


def emit_last_prices(last_prices, broadcast=False):
    """Emit last prices to socketio."""
    last_prices_json = get_last_prices_json(last_prices)
    socketio.emit('json', last_prices_json,
                  namespace='/lastpriceslive', broadcast=broadcast)


@socketio.on('connect', namespace='/lastpriceslive')
def last_prices(broadcast=False):
    """Send the last price to the client."""
    last_prices = LastPrice.query.all()
    emit_last_prices(last_prices, broadcast=broadcast)


def broadcast_last_prices():
    """Send the last price to all the clients."""
    last_prices(broadcast=True)
