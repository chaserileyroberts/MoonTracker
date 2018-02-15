from flask import Flask, request, render_template, flash, g
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)

import sqlite3


app = Flask(__name__)


class WebsiteServer():
    class PhoneNumberForm(Form):
        phone_number = StringField('Phone Number', [
            validators.Length(min=10),
            validators.Regexp('^[0-9]+$', message="Input characters must be numeric")])
        asset = SelectField(
            'Coin', choices=[('BTC', 'BTC'), ('ETH', 'ETH'), ('LTC', 'LTC')])
        target_price = IntegerField('Target Price', [validators.optional()])
        less_more = SelectField(
            '', choices=[(1, 'above'), (0, 'below')], coerce=int)

    @staticmethod
    def set_database(file_name):
        WebsiteServer.db_conn = sqlite3.connect(file_name)
        WebsiteServer.db_cursor = WebsiteServer.db_conn.cursor()
        WebsiteServer.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS alerts '
            '(symbol text, price real, above integer, phone_number text)''')
        WebsiteServer.db_conn.commit()
        app = Flask(__name__)
        app.secret_key = '000000'

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = WebsiteServer.PhoneNumberForm(request.form)
        if request.method == 'POST' and form.validate():
            phone_number = form.phone_number.data
            asset = form.asset.data
            target_price = form.target_price.data
            less_more = form.less_more.data

            # Store in database
            cmd = "INSERT INTO alerts VALUES (?, ?, ?, ?)"

            WebsiteServer.db_cursor.execute(
                cmd, (asset, target_price, less_more, phone_number))
            WebsiteServer.db_conn.commit()

        return render_template('index.html', form=form)


if __name__ == '__main__':
    WebsiteServer.set_database('moontracker_database.db')
    app.run()
