from flask import Flask, request, render_template, flash, g
from flask_apscheduler import APScheduler
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)

import sqlite3


app = Flask(__name__)


def check_alerts():
    print("CHECK ALERTS")


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'app:check_alerts',
            'trigger': 'interval',
            'seconds': 10
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

    db_manager = DatabaseManager("moontracker_database.db")

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()

