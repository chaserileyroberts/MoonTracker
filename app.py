from flask import Flask, request, render_template, flash, g
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)

from twilio.rest import Client as TwilioClient
from coinbase.wallet.client import Client as CoinbaseClient
from api_keys import (coinbase_auth, coinbase_secret,
                      twilio_sid, twilio_auth, app_secret)

import sqlite3

coinbase_client = CoinbaseClient(coinbase_auth, coinbase_secret,
                                 api_version='2017-08-07')

twilio_client = TwilioClient(twilio_sid, twilio_auth)

db_conn = sqlite3.connect('moontracker_database.db')
db_cursor = db_conn.cursor()

db_cursor.execute('''CREATE TABLE IF NOT EXISTS alerts
                (symbol text, price real, above integer, phone_number text)''')

db_conn.commit()
app = Flask(__name__)


class PhoneNumberForm(Form):
    phone_number = StringField('Phone Number', [validators.Length(min=10)])
    asset = SelectField(
        'Coin', choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC')])
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhoneNumberForm(request.form)
    if request.method == 'POST' and form.validate():
        phone_number = form.phone_number.data
        asset = form.asset.data
        target_price = form.target_price.data
        less_more = form.less_more.data

        # Store in database
        query = "INSERT INTO alerts VALUES ('{0}', {1}, {2}, '{3}')".format(
            asset, target_price, less_more, phone_number)
        db_cursor.execute(query)
        db_conn.commit()

        # need to send notification when
        # target price is reached
        # price = coinbase_client.get_spot_price(currency='USD')
        # twilio_client.api.account.messages.create(
        #     to=phone_number,
        #     from_="+15072003597",
        #     body="Bitcoin price is: " + price.amount)
        # flash("Sent to " + form.phone_number.data)

    return render_template('index.html', form=form)


app.secret_key = app_secret
