import texter
import pytest


class twilio():

    def __init__(self):
        self.messages = []

    def create(self, to, from_, body):
        self.messages.append(body)


class price():

    def __init__(self, amount):
        self.amount = amount


def test_less_than_text():
    t = twilio()
    clients = [('555-555-5555', '1.0', 'BTC')]
    texter.text_less_than(t.create, clients, price("3.00"))
    assert len(t.messages) == 1
    assert "below" in t.messages[0]
    assert 'BTC' in t.messages[0]


def test_greater_than_text():
    t = twilio()
    clients = [('555-555-5555', '1.0', 'BTC')]
    texter.text_greater_than(t.create, clients, price("3.00"))
    assert len(t.messages) == 1
    assert "above" in t.messages[0]
    assert 'BTC' in t.messages[0]


def test_text_loop():
    pass
    # TODO(Chase): Build this.
