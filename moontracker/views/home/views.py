"""Home related views."""
from datetime import datetime
from flask import request, render_template, flash, Blueprint
from flask_wtf import RecaptchaField, Recaptcha
from flask_login import current_user
from wtforms import Form, FloatField, StringField, SelectField, DateField
from wtforms import validators
import json

from moontracker.assets import supported_assets, assets, market_apis
from moontracker.extensions import db
from moontracker.models import Alert, LastPrice

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Code for the homepage."""
    form = AlertForm(request.form)
    if request.method == 'POST' and form.validate():
        asset = form.asset.data
        target_price = form.target_price.data
        less_more = form.less_more.data
        phone_number = form.phone_number.data
        market = form.market.data
        end_date = form.end_date
        had_last_price_error = False
        if less_more == 2 or less_more == 3:
            last_price_query = LastPrice.query.filter(
                LastPrice.symbol == asset)
            lp_result = last_price_query.one_or_none()
            if lp_result is None:
                had_last_price_error = True
            else:
                if less_more == 2:  # + %
                    less_more = 1  # above
                    target_price = lp_result.price * (
                        target_price / 100.0 + 1.0)
                elif less_more == 3:  # - %
                    less_more = 0  # below
                    target_price = lp_result.price * (
                        1.0 - target_price / 100.0)

        if had_last_price_error:
            flash("Internal error setting percent change!", 'error')
        else:
            alert = Alert(symbol=asset, price=target_price,
                          above=less_more, phone_number=phone_number,
                          market=market, end_date=end_date.data)
            if current_user.is_authenticated:
                alert.user_id = current_user.id

            db.session.add(alert)
            db.session.commit()
            flash("Alert is set!")

    return render_template('index.html', form=form,
                           app_markets_json=json.dumps(supported_assets))


@home_blueprint.route('/appMarkets.js', methods=['GET'])
def app_markets():
    """Generate JavaScript for appMarkets."""
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

    less_more_validators = [validators.AnyOf([1, 0, 2, 3])]
    less_more = SelectField(
        '',
        choices=[(1, 'above'), (0, 'below'), (2, '+ %'), (3, '- %')],
        validators=less_more_validators,
        coerce=int)
    end_date = DateField("Enter end date for alert (YYYY/MM/DD)",
                         format='%Y-%m-%d', default=datetime.now().date())

    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])

    market_validators = [validators.AnyOf([m for m in market_apis])]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)
