"""Home related views."""
from flask import request, render_template, flash, Blueprint
from flask_wtf import RecaptchaField, Recaptcha
from flask_login import current_user
from wtforms import Form
from wtforms import FloatField, StringField, SelectField
from wtforms import validators
from wtforms import widgets
from wtforms.fields import FormField
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
                          market=market)
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


class AlertConditionForm(Form):
    """Form for AlertConditionField."""

    # cond_option_validators = [validators.AnyOf([1, 0, 2, 3])]
    cond_option_validators = [validators.optional()]
    cond_option = SelectField(
        'Condition Option',
        choices=[(1, 'above'), (0, 'below'), (2, '+ %'), (3, '- %')],
        validators=cond_option_validators,
        coerce=int)
    price = FloatField('Target Price')
    percent = FloatField('Target Percent Change')
    percent_duration = SelectField(
        'Target Change Duration',
        choices=[
            (0, '1 hour'),
            (1, '24 hours'),
            (2, '1 week'),
            (3, '1 month')],
        coerce=int)


class AlertConditionWidget(widgets.TableWidget):
    """Table widget that can pass subfield kwargs."""

    def __call__(self, field, subfield_kwargs=None, **kwargs):
        """Generate HTML for the widget."""
        html = []
        if self.with_table_tag:
            kwargs.setdefault('id', field.id)
            html.append('<dl ' + widgets.html_params(**kwargs) + '>')
        hidden = ''
        if subfield_kwargs is None:
            subfield_kwargs = {}
        for subfield in field:
            if subfield.type in ('HiddenField', 'CSRFTokenField'):
                hidden += subfield(**subfield_kwargs)
            else:
                html.append(
                    '<dt>' +
                    subfield.label() +
                    '</dt><dd>' +
                    hidden +
                    subfield(**subfield_kwargs) +
                    '</dd>')
                hidden = ''
        if self.with_table_tag:
            html.append('</dl>')
        if hidden:
            html.append(hidden)
        return widgets.HTMLString(''.join(html))


class AlertConditionField(FormField):
    """Field for alert condition."""

    widget = AlertConditionWidget()

    def __init__(self, label='Alert Condition', validators=None, separator='-',
                 **kwargs):
        """Init."""
        super().__init__(AlertConditionForm, label, validators, **kwargs)


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

    # alert_cond = AlertConditionField('Alert Condition')

    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])

    market_validators = [validators.AnyOf([m for m in market_apis])]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)
