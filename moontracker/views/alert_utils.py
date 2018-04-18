from moontracker.models import Alert
from moontracker.extensions import db
from wtforms import Form
from wtforms import FloatField, StringField, SelectField
from wtforms import validators
from flask_wtf import RecaptchaField, Recaptcha
from moontracker.assets import supported_assets, assets, market_apis
from moontracker.times import supported_times, times
from flask_login import current_user


class AlertForm(Form):
    """Form object for website."""

    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])

    asset = SelectField(
        'Coin', choices=assets)

    market_validators = [validators.AnyOf([m for m in market_apis])]
    market = SelectField('Market',
                         choices=[('', '')] + [(m, m) for m in market_apis],
                         default='', validators=market_validators)

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
        choices=times,
        coerce=int)

    recaptcha = RecaptchaField(
        'Recaptcha', validators=[
            Recaptcha("Please do the recaptcha.")])

    def validate(self, **kwargs):
        """Validate the AlertForm."""
        if self.cond_option.data == 1 or self.cond_option.data == 0:
            self.price.validators = AlertForm.price_validators
            self.percent.validators = [validators.optional()]
            self.percent_duration.validators = [validators.optional()]
        elif self.cond_option.data == 2 or self.cond_option.data == 3:
            self.price.validators = [validators.optional()]
            self.percent.validators = AlertForm.percent_validators
            pdv = AlertForm.percent_duration_validators
            self.percent_duration.validators = pdv

        return super().validate(**kwargs)


def make_new_alert(form):
    """Create new alert.
    Args:
        form: AlertForm Object.
    """
    asset = form.asset.data
    cond_option = form.cond_option.data
    phone_number = form.phone_number.data
    market = form.market.data
    alert = Alert(
        symbol=asset,
        condition=cond_option,
        phone_number=phone_number,
        market=market)
    if cond_option == 1 or cond_option == 0:
        alert.price = form.price.data
    elif cond_option == 2 or cond_option == 3:
        alert.percent = form.percent.data
        # alert.percent_duration = form.percent_duration.data
        alert.percent_duration = 86400  # fix this!

    if current_user.is_authenticated:
        alert.user_id = current_user.id

    db.session.add(alert)
    db.session.commit()


def modify_existing_alert(form):
    pass


def delete_existing_alert(form):
    pass
