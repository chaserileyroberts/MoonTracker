"""
Integration Test.
Make sure posts from the website causes texts to be sent.
"""

from flask import current_app
from moontracker.texter import Texter
from tests import test_texter

test_client = current_app.test_client()


def test_integration_sanity():
    """
    Make post request to the website, make sure texter sends the message.
    """
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='1',
            target_price='1'
        ))
    assert response.status_code == 200
    cb = test_texter.price_tracker_fake("45")
    twilio = test_texter.twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)
    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'above' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '5558675309'


def test_integration_below():
    """
    Make post request to the website, make sure texter sends the message.
    """
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='0',
            target_price='100'
        ))
    assert response.status_code == 200
    cb = test_texter.price_tracker_fake("45")
    twilio = test_texter.twilio_fake()
    texter = Texter()
    texter.set_clients(cb, twilio.send_message)
    texter.check_alerts()
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'below' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '5558675309'
