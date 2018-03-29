"""Home related views."""
from flask import request, render_template, flash, Blueprint
from flask_wtf import RecaptchaField, Recaptcha
from flask_login import current_user
from wtforms import Form, FloatField, StringField, SelectField
from wtforms import validators
import json

from moontracker.assets import supported_assets, assets, market_apis
from moontracker.extensions import db
from moontracker.models import Alert

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Code for the homepage."""
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("Alert is set!")
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
        if form.validate():
            flash("Alert is set!")
            alert = Alert(symbol=product, price=target_price,
                          above=less_more, phone_number=phone_number,
                          market=market)
            if current_user.is_authenticated:
                alert.user_id = current_user.id
            db.session.add(alert)
            db.session.commit()
    return render_template('products.html', form=form,
                           app_markets_json=json.dumps(supported_assets))


class AlertForm(Form):
    """Form object for website."""

    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])
    asset = SelectField(
        'Coin', choices=assets)
    target_price = FloatField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)
    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])


class ProductsForm(Form):
    """Website form for the products page."""

    phone_number_validators = [
        validators.Length(min=10),
        validators.Regexp('^[0-9]+$',
                          message="Input characters must be numeric")
    ]
    phone_number = StringField('Phone Number',
                               validators=phone_number_validators)

    product_choices = [(product, supported_assets[product]['name'])
                       for product in supported_assets]
    product_validators = [validators.InputRequired()]
    product = SelectField('Product',
                          choices=[('', '')] + product_choices,
                          default='',
                          validators=product_validators)

    market_validators = [validators.InputRequired()]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)

    target_price_validators = [validators.InputRequired()]
    target_price = FloatField('Target Price',
                              validators=target_price_validators)

    less_more_choices = [(1, 'above'), (0, 'below')]
    less_more = SelectField('', choices=less_more_choices, coerce=int)
    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])
