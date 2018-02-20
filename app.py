from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)
from texter import Texter

import json


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JOBS = [
        {
            'id': 'job1',
            'func': 'app:check_alerts',
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
texter = Texter()


class AlertForm(Form):
    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])
    asset = SelectField(
        'Coin',
        choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('LTC', 'Litecoin')])
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    above = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)


def check_alerts():
    with app.app_context():
        texter.check_alerts(db)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        asset = form.asset.data
        target_price = form.target_price.data
        less_more = form.less_more.data
        phone_number = form.phone_number.data

        alert = Alert(symbol=asset, price=target_price,
                      above=less_more, phone_number=phone_number)
        db.session.add(alert)
        db.session.commit()

    return render_template('index.html', form=form)


app_markets = {
    'coinbase': {
        'name': 'Coinbase',
        'products': [
            ('btc-usd', 'Bitcoin/USD'),
            ('eth-usd', 'Ethereum/USD'),
            ('ltc-usd', 'Litecoin/USD')
        ]
    }
}


class MarketsForm(Form):
    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])
    market_choices = [(market_key, market['name'])
                      for market_key, market in app_markets.items()]
    market = SelectField('Market', choices=[('', '')] + market_choices,
                         default='')
    product = SelectField('Product', choices=[('', '')], default='')
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)


@app.route('/markets', methods=['GET', 'POST'])
def markets():
    form = MarketsForm(request.form)
    if request.method == 'POST' and form.validate():
        phone_number = form.phone_number.data
        market = form.market.data
        product = form.product.data
        target_price = form.target_price.data
        less_more = form.less_more.data

        # TODO: add to database

    return render_template('markets.html', form=form,
                           app_markets_json=json.dumps(app_markets))


if __name__ == '__main__':
    db.create_all()

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run()
