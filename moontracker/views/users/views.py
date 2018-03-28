"""User related views."""
from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import Form, StringField, IntegerField, SelectField, validators
from sqlalchemy import exists

from moontracker.extensions import bcrypt, db, login_manager
from moontracker.models import User, Alert
from moontracker.assets import assets
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
    user_alerts_query = Alert.query.filter(Alert.user_id == current_user.id)
    alerts = []
    for alert in user_alerts_query.all():
        alerts.append(AlertDisplay(alert))

    form = AlertForm(request.form)

    # this should change depending on which edit button is clicked
    if (user_alerts_query.count() > 0):
        current_alert = user_alerts_query[0]
        form = AlertForm(request.form, phone_number=current_alert.phone_number,
            asset=current_alert.symbol, target_price=current_alert.price, less_more=current_alert.above)

    if request.method == 'POST':
        if request.form['submit'] == 'Delete':
            print('delete button pressed')
            db.session.delete(current_alert)
            db.session.commit()
            # figure out proper way to refresh
        elif request.form['submit'] == 'Save Changes':
            current_alert.phone_number = form.phone_number.data
            current_alert.symbol = form.asset.data
            # current_alert.price = form.target_price.data
            current_alert.above = form.less_more.data
            db.session.commit()
            print('update button pressed')
            # figure out proper way to refresh

    return render_template('manage.html', alerts=alerts, form=form)


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


class AlertDisplay():
    """Alert information object."""
    def __init__(self, alert):
        self.phone_number = alert.phone_number
        self.asset = alert.symbol
        if alert.above == 1:
            self.above = 'above'
        else:
            self.above = 'below'
        self.target_price = alert.price
