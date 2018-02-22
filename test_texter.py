from texter import Texter
from app import Alert, db
import pytest
import os
from unittest.mock import MagicMock as Mock
import twilio
import pytest
from price_tracker import PriceTracker


class twilio_fake():

    def __init__(self):
        self.to = []
        self.messages = []

    def send_message(self, to, from_, body):
        self.to.append(to)
        self.messages.append(body)


class price_tracker_fake():

    def __init__(self, amount):
        self.amount = float(amount)

    def get_spot_price(self, asset):
        return self.amount


def setup():
    db.drop_all()
    db.create_all()


def teardown():
    db.drop_all()


def test_less_than_text():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alerts = [Alert(symbol='BTC', price=50.0, above=0,
                    phone_number='555-555-5555')]

    texter.text_less_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert "below" in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert len(twilio.to) == 1
    assert twilio.to[0] == '555-555-5555'


def test_greater_than_text():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alerts = [Alert(symbol='BTC', price=1.0, above=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert "above" in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert len(twilio.to) == 1
    assert twilio.to[0] == '555-555-5555'


def test_LTC():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alerts = [Alert(symbol='LTC', price=1.0, above=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert 'LTC' in twilio.messages[0]


def test_ETH():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alerts = [Alert(symbol='ETH', price=1.0, above=1,
                    phone_number='555-555-5555')]

    texter.text_greater_than(alerts, 3.0)
    assert len(twilio.messages) == 1
    assert 'ETH' in twilio.messages[0]


def test_empty_text_loop():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    texter.check_alerts(db)
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0


def test_single_text_loop():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alert = Alert(symbol='BTC', price=10.0, above=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts(db)
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'above' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '555-555-5555'


def test_single_text_loop_below():
    cb = price_tracker_fake("5")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)

    alert = Alert(symbol='BTC', price=10.0, above=0,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts(db)
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'below' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '555-555-5555'


def test_single_entry_no_text():
    cb = price_tracker_fake("45")
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)
    alert = Alert(symbol='BTC', price=100.0, above=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts(db)
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0


def test_invalid_number(capsys):
    cb = price_tracker_fake("45")
    send_message = Mock()
    send_message.side_effect = (twilio.base.exceptions
                                .TwilioRestException(Mock(), Mock()))
    texter = Texter()
    texter.set_clients(cb, send_message)
    alert = Alert(symbol='BTC', price=10.0, above=1,
                  phone_number='5555')
    db.session.add(alert)
    db.session.commit()
    texter.check_alerts(db)
    out, err = capsys.readouterr()
    assert "Invalid number" in out


def test_invalid_number_below(capsys):
    cb = price_tracker_fake("45")
    send_message = Mock()
    send_message.side_effect = (twilio.base.exceptions
                                .TwilioRestException(Mock(), Mock()))
    texter = Texter()
    texter.set_clients(cb, send_message)
    alert = Alert(symbol='BTC', price=100.0, above=0,
                  phone_number='5555')
    db.session.add(alert)
    db.session.commit()
    texter.check_alerts(db)
    out, err = capsys.readouterr()
    assert "Invalid number" in out


def test_price_tracker_integration():
    cb = PriceTracker()
    twilio = twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)
    alert = Alert(symbol='BTC', price=100.0, above=1,
                  phone_number='555-555-5555')
    db.session.add(alert)
    db.session.commit()

    texter.check_alerts(db)
