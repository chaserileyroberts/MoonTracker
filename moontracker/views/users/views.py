"""User related views."""
from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required
from wtforms import Form, StringField, IntegerField, SelectField, validators
from sqlalchemy import exists

from moontracker.extensions import bcrypt, db, login_manager
from moontracker.models import User
from moontracker.assets import assets

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
    num_forms = range(3)  # will be number of users alerts
    forms = []
    coins = ['BTC', 'ETH', 'LTC']
    for i in num_forms:
        forms.append(ManageAlertForm(
            request.form, asset=coins[i % 3], less_more=i % 2, target_price=i))
    # I need to not let this update every alert on page
    for form in forms:
        if request.method == 'POST' and form.validate():
            asset = form.asset.data
            target_price = form.target_price.data
            less_more = form.less_more.data

    return render_template('manage.html', forms=forms)


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


# this can probably be replaced by previously written alert form
# for logged in user
class ManageAlertForm(Form):
    """Manage Alert Form object."""

    asset = SelectField(
        'Coin', choices=assets)
    target_price = IntegerField('Target Price', [validators.optional()])
    less_more = SelectField(
        '', choices=[(1, 'above'), (0, 'below')], coerce=int)
