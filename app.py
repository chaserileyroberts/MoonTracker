from flask import Flask, request, render_template, flash, g
from wtforms import Form, StringField, IntegerField, SelectField, validators

from twilio.rest import Client as TwilioClient
from coinbase.wallet.client import Client as CoinbaseClient
from api_keys import coinbase_auth, coinbase_secret, twilio_sid, twilio_auth, app_secret

import sqlite3

coinbase_client = CoinbaseClient(coinbase_auth, coinbase_secret,
    api_version='2017-08-07')

twilio_client = TwilioClient(twilio_sid, twilio_auth)

class PhoneNumberForm(Form):
    phone_number = StringField('Phone Number', [validators.Length(min=10)])
    target_price = IntegerField('Bitcoin Target Price', [validators.optional()])
    less_more= SelectField('', choices=[('>='), ('<=')])

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('') # path to database
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhoneNumberForm(request.form)
    if request.method == 'POST' and form.validate():
        # need to store in database and send notification when
        # target price is reached
        phone_number = form.phone_number.data
        target_price = form.target_price.data
        price = coinbase_client.get_spot_price(currency='USD')
        twilio_client.api.account.messages.create(
            to=phone_number,
            from_="+15072003597",
            body="Bitcoin price is: " + price.amount)
        flash("Sent to " + form.phone_number.data)
    
    return render_template('index.html', form=form)

app.secret_key = app_secret
