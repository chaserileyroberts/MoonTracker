"""Texting Service."""
from twilio.rest import Client as TwilioClient
import twilio

from moontracker.price_tracker import PriceTracker
from moontracker.assets import supported_assets
from moontracker.times import supported_times
from moontracker.extensions import db
from moontracker.models import Alert, LastPrice

from datetime import datetime


class Texter(object):
    """Texting Object."""

    def __init__(self):
        """Object initializer."""
        self.price_tracker = None
        self.send_message = None

    def set_clients(self, price_tracker=None, send_message=None):
        """Set Clients. Used for unit testing.

        Args:
            price_tracker: The price tracking client.
            send_message: The function to send the text message.
        """
        self.price_tracker = price_tracker
        self.send_message = send_message

    def check_alerts(self):
        """Check alerts for all types of assets."""
        if self.price_tracker is None:
            self.price_tracker = PriceTracker()
        if self.send_message is None:
            from moontracker.api_keys import twilio_sid, twilio_auth
            twilio_client = TwilioClient(twilio_sid, twilio_auth)
            self.send_message = twilio_client.api.account.messages.create

        for asset in supported_assets:
            for market in supported_assets[asset]["markets"]:
                self.check_alerts_for_coin(asset, market)

        # too many requests per second, keep getting 429 code
        for asset in supported_assets:
            for market in supported_assets[asset]["markets"]: # This might change for percent change
                for time in supported_times:
                    self.check_alerts_for_coin_percent(asset, market, time[1])

    def check_alerts_for_coin(self, coin, market):
        """Check for alerts.

        Args:
            coin: The asset to check against.
            market: String of which market to use
        """
        timestamp = datetime.utcnow()

        # Make the request
        price = self.price_tracker.get_spot_price(
            asset=coin, market=market)

        # Get all of the prices that are less than the current amount
        greater_than_query = Alert.query.filter(
            Alert.symbol == coin,
            Alert.price < price,
            Alert.condition == 1,
            ((Alert.market == market) | (Alert.market.is_(None))))
        self.text_greater_than(greater_than_query.all(), price)
        greater_than_query.delete(False)

        less_than_query = Alert.query.filter(
            Alert.symbol == coin,
            Alert.price > price,
            Alert.condition == 0,
            ((Alert.market == market) | (Alert.market.is_(None))))
        self.text_less_than(less_than_query.all(), price)
        less_than_query.delete(False)

        last_price = LastPrice(symbol=coin, price=price, timestamp=timestamp)
        db.session.merge(last_price)

        # TODO(Chase): This will cause race condition.
        db.session.commit()

    def check_alerts_for_coin_percent(self, coin, market, duration):
        """Check for alerts.

        Args:
            coin: The asset to check against.
            market: String of which market to use
        """
        timestamp = datetime.utcnow()

        # I need to check each supported time
        percent = self.price_tracker.get_percent_change(
           asset=coin, market=market, duration=duration)

        price = self.price_tracker.get_spot_price(
            asset=coin, market=market)

        if (percent > 0): # what if 0? did we already check for that?
            # Get all of the alerts with a percent increase less than the current percent increase
            percent_increase_query = Alert.query.filter(
                Alert.symbol == coin,
                Alert.percent_duration == duration,
                Alert.percent < percent,
                Alert.condition == 2,
                ((Alert.market == market) | (Alert.market.is_(None))))
            self.text_percent_increase(percent_increase_query.all(), price, percent, duration)
            percent_increase_query.delete(False)
        else:
            # Get all of the alerts with a percent decrease smaller in magnitude than the current percent decrease
            percent_decrease_query = Alert.query.filter(
                Alert.symbol == coin,
                Alert.percent_duration == duration,
                - Alert.percent > percent,
                Alert.condition == 3,
                ((Alert.market == market) | (Alert.market.is_(None))))
            self.text_percent_decrease(percent_decrease_query.all(), price, percent, duration)
            percent_decrease_query.delete(False)

        # What is last price doing and do I need it?

        # TODO(Chase): This will cause race condition.
        db.session.commit()

    def text_greater_than(self, alerts, price):
        """Send text message for above triggers.

        Args:
            alerts: The alerts to send. Should be type Alert.
            price: The current asset price.
        """
        for alert in alerts:
            # Some logging
            print("Sending text to %s" % alert.phone_number)
            try:
                # Send the text
                self.send_message(
                    to=alert.phone_number,
                    from_="+15072003597",
                    body=(
                        "%s price is above your trigger of %s. "
                        "Current price is %s"
                        % (alert.symbol, alert.price, price)))
            except twilio.base.exceptions.TwilioRestException:
                # Catch errors.
                print("Invalid number:", alert.phone_number)

    def text_less_than(self, alerts, price):
        """Send text message for above triggers.

        Args:
            alerts: The alerts to send. Should be type Alert.
            price: The current asset price.
        """
        for alert in alerts:
            # Some logging
            print("Sending text to %s" % alert.phone_number)
            try:
                # Send the text
                self.send_message(
                    to=alert.phone_number,
                    from_="+15072003597",
                    body=(
                        "%s price is below your trigger of %s. "
                        "Current price is %s"
                        % (alert.symbol, alert.price, price)))
            except twilio.base.exceptions.TwilioRestException:
                print("Invalid number:", alert.phone_number)

    def text_percent_increase(self, alerts, price, percent, percent_duration):
        """Send text message for percent increase triggers.

        Args:
            alerts: The alerts to send. Should be type Alert.
            price: The current asset price.
            percent:
            percent_duration:
        """
        for alert in alerts:
            print("Sending text to %s" % alert.phone_number)
            try:
                self.send_message(
                    to=alert.phone_number,
                    from_="+15072003597",
                    body=(
                        "%s price has increased by at least %s%% over %d hours. "
                        "Current price is %s"
                        % (alert.symbol, alert.price, percent, percent_duration, price)))
            except twilio.base.exceptions.TwilioRestException:
                print("Invalid number:", alert.phone_number)

    def text_percent_decrease(self, alerts, price, percent, percent_duration):
        """Send text message for percent decrease triggers.

        Args:
            alerts: The alerts to send. Should be type Alert.
            price: The current asset price.
            percent:
            percent_duration:
        """
        for alert in alerts:
            print("Sending text to %s" % alert.phone_number)
            try:
                self.send_message(
                    to=alert.phone_number,
                    from_="+15072003597",
                    body=(
                        "%s price has decreased by at least %s%% over %d hours. "
                        "Current price is %s"
                        % (alert.symbol, alert.price, percent, percent_duration, price)))
            except twilio.base.exceptions.TwilioRestException:
                print("Invalid number:", alert.phone_number)
