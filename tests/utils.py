"""Utility functions and classes for test modules."""
from flask import current_app
from selenium import webdriver

test_client = current_app.test_client()
browser = webdriver.ChromeOptions()


def register(username, password, phone_number):
    """Register user with specified username, password, and phone number."""
    return test_client.post('/create', data=dict(
        username=username,
        password=password,
        phone_number=phone_number
    ), follow_redirects=True)


def login(username, password):
    """Login user with specified username and password."""
    return test_client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)


def logout():
    """Logout."""
    return test_client.get('/logout', follow_redirects=True)


class twilio_fake():
    """Fake twilio client."""

    def __init__(self):
        """Create the fake twilio client."""
        self.to = []
        self.messages = []

    def send_message(self, to, from_, body):
        """Send a fake message.

        Args:
            to: The number that will recieve the message.
            from_: The number that will send the message.
            body: Text message body.
        """
        self.to.append(to)
        self.messages.append(body)


class price_tracker_fake():
    """Fake Price Tracker client."""

    def __init__(self, amount):
        """Build fake price tracker client."""
        self.amount = float(amount)

    def get_spot_price(self, asset, market):
        """Get the current price of the asset.

        Args:
            asset: The asset in question.
        """
        return self.amount
