from flask import Flask, request, render_template, flash, g
from flask_apscheduler import APScheduler
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)

import sqlite3
from texter import Texter


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:check_alerts',
            'trigger': 'interval',
            'seconds': 2
        }
    ]

    SCHEDULER_API_ENABLED = True


class AlertForm(Form):
    phone_number = StringField('Phone Number', [validators.Length(min=10)])
    asset = SelectField(
        'Coin', choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('LTC', 'Litecoin')])
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)


class DatabaseManager(object):
    def __init__(self):
        self.initialize_database("moontracker_database.db")

    def initialize_database(self, file_name):
        self.db_conn = sqlite3.connect(file_name)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS alerts '
            '(symbol text, price real, above integer, phone_number text)''')
        self.db_conn.commit()


app = Flask(__name__)
db_manager = DatabaseManager()
texter = Texter()


def check_alerts():
    db_conn = sqlite3.connect("moontracker_database.db")
    db_cursor = db_conn.cursor()
    texter.check_alerts(db_conn, db_cursor)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        phone_number = form.phone_number.data
        asset = form.asset.data
        target_price = form.target_price.data
        less_more = form.less_more.data

        # Store in database
        cmd = "INSERT INTO alerts VALUES (?, ?, ?, ?)"

        db_manager.db_cursor.execute(
            cmd, (asset, target_price, less_more, phone_number))
        db_manager.db_conn.commit()

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.config.from_object(Config())
    app.secret_key = '000000'

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
