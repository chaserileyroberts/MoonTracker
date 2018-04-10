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
        market = form.market.data
        alert = Alert(symbol=asset, price=target_price,
                      above=less_more, phone_number=phone_number,
                      market=market)
        if current_user.is_authenticated:
            alert.user_id = current_user.id

        db.session.add(alert)
        db.session.commit()

    return render_template('index.html', form=form,
                           app_markets_json=json.dumps(supported_assets))


@home_blueprint.route('/appMarkets.js', methods=['GET'])
def app_markets():
    """Generates JavaScript for appMarkets."""
    return 'appMarkets = ' + json.dumps(supported_assets)


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
    less_more = SelectField('', choices=[(1, 'above'), (0, 'below'),
                                         (2, '+ %'), (3, '- %')], coerce=int)
    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])
    market_validators = [validators.InputRequired()]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)
