from twilio.rest import Client as TwilioClient
from coinbase.wallet.client import Client as CoinbaseClient
from api_keys import *
coinbase_client = CoinbaseClient(
  coinbase_auth,
  coinbase_secret,
  api_version='2017-08-07')

currency_code = 'USD'  # can also use EUR, CAD, etc.

chase_numbers = ["+15074615169"]
# Make the request
price = coinbase_client.get_spot_price(currency=currency_code)

twilio_client = TwilioClient(twilio_sid, twilio_auth)
for n in chase_numbers:
  twilio_client.api.account.messages.create(
      to=n,
      from_="+15072003597",
      body="Bitcoin price is: %s" % price.amount)

