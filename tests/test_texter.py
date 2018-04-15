from moontracker.texter import Texter
from moontracker.models import Alert
from moontracker.extensions import db
from unittest.mock import MagicMock as Mock
import twilio
from moontracker.price_tracker import PriceTracker
from tests.utils import twilio_fake, price_tracker_fake


def test_less_than_text():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alerts = [Alert(symbol='BTC', price=50.0, condition=0,
                    phone_number='555-555-5555')]

    texter.text_less_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert "below" in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert len(twilio.to) == 1
    assert twilio.to[0] == '555-555-5555'


def test_greater_than_text():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alerts = [Alert(symbol='BTC', price=1.0, condition=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert "above" in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert len(twilio.to) == 1
    assert twilio.to[0] == '555-555-5555'


def test_LTC():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alerts = [Alert(symbol='LTC', price=1.0, condition=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert 'LTC' in twilio.messages[0]


def test_ETH():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alerts = [Alert(symbol='ETH', price=1.0, condition=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert 'ETH' in twilio.messages[0]


def test_empty_text_loop():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    texter.check_alerts()
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0


def test_single_text_loop():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alert = Alert(symbol='BTC', price=10.0, condition=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'above' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '555-555-5555'


def test_single_text_loop_below():
    price_tracker = price_tracker_fake("5")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alert = Alert(symbol='BTC', price=10.0, condition=0,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'below' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '555-555-5555'


def test_single_text_loop_include_market():
    price_tracker = price_tracker_fake("5")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alert = Alert(symbol='ETH', price=2483.0, condition=0,
                  phone_number='1234567890', market='coinbase')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'below' in twilio.messages[0]
    assert 'ETH' in twilio.messages[0]
    assert twilio.to[0] == '1234567890'


def test_include_market_above():
    price_tracker = price_tracker_fake("5")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)

    alert = Alert(symbol='ETH', price=2, condition=1,
                  phone_number='1234567890', market='coinbase')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'above' in twilio.messages[0]
    assert 'ETH' in twilio.messages[0]
    assert twilio.to[0] == '1234567890'


def test_single_entry_no_text():
    price_tracker = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)
    alert = Alert(symbol='BTC', price=100.0, condition=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0


def test_invalid_number(capsys):
    price_tracker = price_tracker_fake("45")
    send_message = Mock()
    send_message.side_effect = (twilio.base.exceptions
                                .TwilioRestException(Mock(), Mock()))
    texter = Texter()
    texter.set_clients(price_tracker, send_message)
    alert = Alert(symbol='BTC', price=10.0, condition=1,
                  phone_number='5555')
    db.session.add(alert)
    db.session.commit()
    texter.check_alerts()
    out, err = capsys.readouterr()
    assert "Invalid number" in out


def test_invalid_number_below(capsys):
    price_tracker = price_tracker_fake("45")
    send_message = Mock()
    send_message.side_effect = (twilio.base.exceptions
                                .TwilioRestException(Mock(), Mock()))
    texter = Texter()
    texter.set_clients(price_tracker, send_message)
    alert = Alert(symbol='BTC', price=100.0, condition=0,
                  phone_number='5555')
    db.session.add(alert)
    db.session.commit()
    texter.check_alerts()
    out, err = capsys.readouterr()
    assert "Invalid number" in out


def test_price_tracker_integration():
    price_tracker = PriceTracker()
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(price_tracker, twilio.send_message)
    alert = Alert(symbol='BTC', price=100.0, condition=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts()
