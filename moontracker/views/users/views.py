"""User related views."""
from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
import wtforms
from wtforms import Form, FloatField, StringField, IntegerField, SelectField
from wtforms import validators
from sqlalchemy import exists

from moontracker.extensions import bcrypt, db, login_manager
from moontracker.models import User, Alert
from moontracker.assets import assets, supported_assets
from moontracker.views.home.views import AlertForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        registered_user = User.query.filter_by(username=username).first()

        if (registered_user is None or
            not bcrypt.check_password_hash(registered_user.pw_hash,
                                           password)):
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('.login'))

        # second argument adds remember me cookie
        login_user(registered_user, True)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    """Logout post request."""
    logout_user()
    return redirect('/')


@users_blueprint.route('/create', methods=['GET', 'POST'])
def create_account():
    """Create new account page."""
    form = NewAccountForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        phone_number = form.phone_number.data

        if db.session.query(exists().where(User.username ==
                                           username)).scalar():
            flash('Username not available', 'error')
            return redirect(url_for('.create_account'))

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username, pw_hash, phone_number)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        flash('Successfully created new account for ' + username)
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('create_account.html', form=form)


@users_blueprint.route('/manage', methods=['GET', 'POST'])
@login_required
def manage_alerts():
    """Manage alerts page."""
    alerts = Alert.query.filter(Alert.user_id == current_user.id).all()

    form = ManageAlertForm(request.form, alerts)
    print(form.alert_id.validators)

    if request.method == 'POST':
        print(request.form['submit'], request.form['submit'] == 'Delete', form.alert_id.data, [
              alert.id for alert in alerts], form.alert_id.validate(form))
        if request.form['submit'] == 'Delete' and form.alert_id.validate(form):
            print('delete button pressed')
            current_index = None
            current_alert = None
            for index, alert in enumerate(alerts):
                if alert.id == int(form.alert_id.data):
                    current_index = index
                    current_alert = alert
                    break

            if current_alert is not None:
                db.session.delete(current_alert)
                db.session.commit()
                del alerts[current_index]

        elif request.form['submit'] == 'Save Changes' and form.validate():
            print('update button pressed')
            current_alert = None
            for alert in alerts:
                if alert.id == int(form.alert_id.data):
                    current_alert = alert
                    break

            if current_alert is not None:
                current_alert.phone_number = form.phone_number.data
                current_alert.symbol = form.asset.data
                current_alert.price = form.target_price.data
                current_alert.above = form.less_more.data
                db.session.merge(current_alert)
                db.session.commit()
                # figure out proper way to refresh
        else:
            print(form.alert_id.errors)

    return render_template('manage.html', alerts=alerts,
                           supported_assets=supported_assets, form=form)


@login_manager.user_loader
def load_user(id):
    """Get the current user's id."""
    return User.query.get(int(id))


class LoginForm(Form):
    """Login Form object."""

    username = StringField('Username', [
        validators.Length(
            min=1, message="Please enter username")])
    password = StringField('Password', [
        validators.Length(min=8, message="Please enter password")])


class NewAccountForm(Form):
    """New Account Form object."""

    username = StringField('Username', [
        validators.Length(
            min=1, message="Please enter username")])
    password = StringField('Password', [
        validators.Length(
            min=8, message="Password must be at least 8 characters")])
    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])


class ManageAlertForm(Form):
    """Form to manage an alert"""

    alert_id = IntegerField(validators=[validators.Required()],
                            widget=wtforms.widgets.HiddenInput())
    phone_number = StringField(
        'Phone Number', [
            validators.Length(min=10),
            validators.Regexp('^[0-9]+$', message="Input characters must be numeric")])
    asset = SelectField(
        'Coin', choices=assets)
    target_price = FloatField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)

    def __init__(self, form, alerts):
        super().__init__(form)
        self.alert_id.validators = [
            validators.AnyOf([alert.id for alert in alerts])]
