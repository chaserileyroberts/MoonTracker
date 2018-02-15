import texter
import pytest
import sqlite3
import os


class twilio_fake():

    def __init__(self):
        self.to = []
        self.messages = []

    def send_message(self, to, from_, body):
        self.to.append(to)
        self.messages.append(body)


class price():

    def __init__(self, amount):
        self.amount = amount


class coinbase_fake():

    def __init__(self, amount):
        self.amount = amount

    def get_spot_price(self, currency_pair):
        return price(self.amount)


def setup():
    db_conn = sqlite3.connect('test.db')
    db_cursor = db_conn.cursor()
    db_cursor.execute(
        'CREATE TABLE IF NOT EXISTS alerts '
        '(symbol text, price real, above integer, phone_number text)''')
    db_conn.commit()


def teardown():
    # TODO(Chase): Create temp directory for the test.db file.
    os.remove('test.db')


def test_less_than_text():
    t = twilio_fake()
    clients = [('555-555-5555', '1.0', 'BTC')]
    texter.text_less_than(t.send_message, clients, price("3.00"))
    assert len(t.messages) == 1
    assert "below" in t.messages[0]
    assert 'BTC' in t.messages[0]
    assert len(t.to) == 1
    assert t.to[0] == '555-555-5555'


def test_greater_than_text():
    t = twilio_fake()
    clients = [('555-555-5555', '1.0', 'BTC')]
    texter.text_greater_than(t.send_message, clients, price("3.00"))
    assert len(t.messages) == 1
    assert "above" in t.messages[0]
    assert 'BTC' in t.messages[0]
    assert len(t.to) == 1
    assert t.to[0] == '555-555-5555'


def test_LTC():
    t = twilio_fake()
    clients = [('555-555-5555', '1.0', 'LTC')]
    texter.text_greater_than(t.send_message, clients, price("3.00"))
    assert len(t.messages) == 1
    assert 'LTC' in t.messages[0]


def test_empty_text_loop():
    cb = coinbase_fake("45.00")
    twilio = twilio_fake()
    db_connection = sqlite3.connect('test.db')
    texter.text_loop(cb, twilio.send_message, db_connection, "BTC")
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0


def test_single_text_loop():
    cb = coinbase_fake("45.00")
    twilio = twilio_fake()
    db_connection = sqlite3.connect('test.db')
    db_cursor = db_connection.cursor()
    cmd = "INSERT INTO alerts VALUES (?, ?, ?, ?)"
    db_cursor.execute(
        cmd, ("BTC", 100.0, 0, "555-555-5555"))
    db_connection.commit()
    texter.text_loop(cb, twilio.send_message, db_connection, "BTC")
    assert len(twilio.messages) == 1
    assert len(twilio.to) == 1
    assert 'below' in twilio.messages[0]
    assert 'BTC' in twilio.messages[0]
    assert twilio.to[0] == '555-555-5555'


def test_single_entry_no_text():
    cb = coinbase_fake("45.00")
    twilio = twilio_fake()
    db_connection = sqlite3.connect('test.db')
    db_cursor = db_connection.cursor()
    cmd = "INSERT INTO alerts VALUES (?, ?, ?, ?)"
    db_cursor.execute(
        cmd, ("BTC", 100.0, 1, "555-555-5555"))
    db_connection.commit()
    texter.text_loop(cb, twilio.send_message, db_connection, "BTC")
    assert len(twilio.messages) == 0
    assert len(twilio.to) == 0
