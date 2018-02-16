"""
Integration Test.
Make sure posts from the website causes texts to be sent.
"""

import flask
import app
import time
import texter
import pytest
import sqlite3
import os
import test_texter

test_client = app.app.test_client()


def setup():
    # TODO(Chase): Setup tempfile.
    app.WebsiteServer.set_database('test.db')


def teardown():
    os.remove('test.db')


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
    cb = test_texter.coinbase_fake("45.00")
    twilio = test_texter.twilio_fake()
    db_connection = sqlite3.connect('test.db')
    texter.text_loop(cb, twilio.send_message, db_connection, "BTC")
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'above' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '5558675309'
