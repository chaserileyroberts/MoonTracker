"""Home related views."""
from flask import request, render_template, flash, Blueprint
from flask_wtf import RecaptchaField, Recaptcha
from flask_login import current_user
from wtforms import Form, StringField, IntegerField, SelectField, validators
import json

from moontracker.assets import assets
from moontracker.extensions import db
from moontracker.models import Alert

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Code for the homepage."""
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("Success!")
        asset = form.asset.data
        target_price = form.target_price.data
        less_more = form.less_more.data
        phone_number = form.phone_number.data

        alert = Alert(symbol=asset, price=target_price,
                      above=less_more, phone_number=phone_number)
        if current_user.is_authenticated:
            alert.user_id = current_user.id

        db.session.add(alert)
        db.session.commit()

    return render_template('index.html', form=form)


@home_blueprint.route('/markets', methods=['GET', 'POST'])
def route_markets():
    """Webpage for the route markets."""
    form = MarketsForm(request.form)
    if request.method == 'POST':
        phone_number = form.phone_number.data
        market = form.market.data
        product = form.product.data
        target_price = form.target_price.data
        less_more = form.less_more.data

        if market:
            product_choices = app_markets[market]['products']
            form.product.choices = [('', '')] + product_choices

        if form.validate():
            # TODO: add to database
            pass

    return render_template('markets.html', form=form,
                           markets_json=json.dumps(markets),
                           products_json=json.dumps(products))


@home_blueprint.route('/products', methods=['GET', 'POST'])
def route_products():
    """Webpage for the products page."""
    form = ProductsForm(request.form)
    if request.method == 'POST':
        phone_number = form.phone_number.data
        product = form.product.data
        market = form.market.data
        target_price = form.target_price.data
        less_more = form.less_more.data

        if product:
            market_choices = []
            for market in markets:
                if product in market['products']:
                    market_choices.append(market)

            form.market.choices = [('', '')] + market_choices

        if form.validate():
            # TODO: add to database
            pass

    return render_template('products.html', form=form,
                           markets_json=json.dumps(markets),
                           products_json=json.dumps(products),
                           app_markets_json=json.dumps(app_markets))


class AlertForm(Form):
    """Form object for website."""

    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])
    asset = SelectField(
        'Coin', choices=assets)
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)
    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])


markets = {
    'coinbase': {
        'name': 'Coinbase',
        'products': [
            'btc-usd',
            'eth-usd',
            'ltc-usd'
        ]
    }
}

products = {
    'btc-usd': {
        'name': 'Bitcoin/USD'
    },
    'eth-usd': {
        'name': 'Ethereum/USD'
    },
    'ltc-usd': {
        'name': 'Litecoin/USD'
    }
}

app_markets = ['coinbase']

app_products = ['btc-usd', 'eth-usd', 'ltc-usd']


class MarketsForm(Form):
    """Website forms that includes market with asset."""

    phone_number_validators = [
        validators.Length(min=10),
        validators.Regexp('^[0-9]+$',
                          message="Input characters must be numeric")
    ]
    phone_number = StringField('Phone Number',
                               validators=phone_number_validators)

    market_choices = [(market, markets[market]['name'])
                      for market in app_markets]
    market_validators = [validators.InputRequired()]
    market = SelectField('Market', choices=[('', '')] + market_choices,
                         default='', validators=market_validators)

    product_validators = [validators.InputRequired()]
    product = SelectField('Product', choices=[('', '')], default='',
                          validators=product_validators)

    target_price_validators = [validators.InputRequired()]
    target_price = IntegerField('Target Price',
                                validators=target_price_validators)

    less_more_choices = [(1, 'above'), (0, 'below')]
    less_more = SelectField('', choices=less_more_choices, coerce=int)


class ProductsForm(Form):
    """Website form for the products page."""

    phone_number_validators = [
        validators.Length(min=10),
        validators.Regexp('^[0-9]+$',
                          message="Input characters must be numeric")
    ]
    phone_number = StringField('Phone Number',
                               validators=phone_number_validators)

    product_choices = [(product, products[product]['name'])
                       for product in app_products]
    product_validators = [validators.InputRequired()]
    product = SelectField('Product',
                          choices=[('', '')] + product_choices,
                          default='',
                          validators=product_validators)

    market_validators = [validators.InputRequired()]
    market = SelectField('Market', choices=[('', '')],
                         default='', validators=market_validators)

    target_price_validators = [validators.InputRequired()]
    target_price = IntegerField('Target Price',
                                validators=target_price_validators)

    less_more_choices = [(1, 'above'), (0, 'below')]
    less_more = SelectField('', choices=less_more_choices, coerce=int)
