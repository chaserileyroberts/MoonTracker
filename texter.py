from twilio.rest import Client as TwilioClient
from coinbase.wallet.client import Client as CoinbaseClient
import twilio
from api_keys import coinbase_auth, coinbase_secret, twilio_sid, twilio_auth, app_secret

import sqlite3
import time

def text_loop(cb_client, twilio_client, db_connection):
  currency_code = 'USD'  # can also use EUR, CAD, etc.
  # Make the request
  price = coinbase_client.get_spot_price(currency=currency_code)
  db_cursor = db_connection.cursor()
  # Get all of the prices that are less than the current amount
  stuff = db_cursor.execute(
      'SELECT phone_number FROM alerts where price < %s' % price.amount)
  for s in stuff:
    # Some logging
    print("Sending text to %s"% s[0])
    try:
      # Send the text
      twilio_client.api.account.messages.create(
        to=s[0],
        from_="+15072003597",
        body="Bitcoin price is: %s" % price.amount)
    except twilio.base.exceptions.TwilioRestException:
      # Catch errors.
      print("Invalid number %s", s[0])
  # Delete values we sent texts to.
  # TODO(Chase): This will cause race condition.
  db_cursor.execute('DELETE FROM alerts where price > 0')
  db_connection.commit()

if __name__ == '__main__':
  coinbase_client = CoinbaseClient(
      coinbase_auth,
      coinbase_secret,
      api_version='2017-05-19')
  twilio_client = TwilioClient(twilio_sid, twilio_auth)
  db_connection = sqlite3.connect('moontracker_database.db')
  while True:
    text_loop(coinbase_client, twilio_client, db_connection)
    time.sleep(1)