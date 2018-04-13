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
        cond_option = form.alert_cond.cond_option.data
        phone_number = form.phone_number.data
        market = form.market.data
        alert = Alert(
            symbol=asset,
            condition=cond_option,
            phone_number=phone_number,
            market=market)
        if cond_option == 1 or cond_option == 0:
            alert.price = form.alert_cond.price.data
        elif cond_option == 2 or cond_option == 3:
            alert.percent = form.alert_cond.percent.data
            alert.percent_duration = form.alert_cond.percent_duration.data

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

    cond_option_validators = [validators.AnyOf([1, 0, 2, 3])]
    cond_option = SelectField(
        'Condition Option',
        choices=[
            (-1, ''),
            (1, 'Above a price'),
            (0, 'Below a price'),
            (2, 'Percent increase'),
            (3, 'Percent decrease')],
        validators=cond_option_validators,
        coerce=int)

    price_validators = [validators.InputRequired()]
    price = FloatField('Target Price')

    percent_validators = [validators.InputRequired()]
    percent = FloatField('Target Percent Change')

    percent_duration_validators = [validators.AnyOf([0, 1, 2, 3])]
    percent_duration = SelectField(
        'Target Change Duration',
        choices=[
            (0, '1 hour'),
            (1, '24 hours'),
            (2, '1 week'),
            (3, '1 month')],
        coerce=int)

    def validate(self, extra_validators=None):
        """Validate the AlertForm."""
        self._errors = None
        success = True
        if self.cond_option.data == 1 or self.cond_option.data == 0:
            self.price.validators = AlertConditionForm.price_validators
            self.percent.validators = [validators.optional()]
            self.percent_duration.validators = [validators.optional()]
        elif self.cond_option.data == 2 or self.cond_option.data == 3:
            self.price.validators = [validators.optional()]
            self.percent.validators = AlertConditionForm.percent_validators
            self.percent_duration.validators = AlertConditionForm.percent_duration_validators

        for name, field in self._fields.items():
            if extra_validators is not None and name in extra_validators:
                extra = extra_validators[name]
            else:
                extra = tuple()
            if not field.validate(self, extra):
                success = False
        return success


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

    alert_cond = AlertConditionField('Alert Condition')

    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])

    market_validators = [validators.AnyOf([m for m in market_apis])]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)
