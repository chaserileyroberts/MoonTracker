from flask import Flask, request, render_template, flash, g
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)

import sqlite3

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
        cmd = "INSERT INTO alerts VALUES (?, ?, ?, ?)"

        db_cursor.execute(
            cmd, (asset, target_price, less_more, phone_number))
        db_conn.commit()

    return render_template('index.html', form=form)


app.secret_key = '000000'
