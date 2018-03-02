"""Website server module."""
from flask import Flask, request, render_template, flash, redirect, url_for, \
    Blueprint
from moontracker.extensions import scheduler, bcrypt, login_manager, db
from sqlalchemy import exists
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)
from moontracker.texter import Texter
from flask_wtf import RecaptchaField, Recaptcha
import json
from datetime import datetime
from moontracker.assets import assets
from flask_login import login_user, logout_user, login_required

blueprint = Blueprint('user', __name__)
texter = Texter()


def create_app(config):
    """Create app with specified config."""
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    texter.set_clients()
    scheduler.start()

    return app


def register_extensions(app):
    """Register all extensions to the Flask application."""
    scheduler.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    db.app = app


def register_blueprints(app):
    """Register all blueprints to the Flask application."""
    app.register_blueprint(blueprint)


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


class Alert(db.Model):
    """Object to add to database."""

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    above = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)


def check_alerts():
    """Check for alerts on the database."""
    with db.app.app_context():
        texter.check_alerts()


@blueprint.route('/', methods=['GET', 'POST'])
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
        db.session.add(alert)
        db.session.commit()

    return render_template('index.html', form=form)


class User(db.Model):
    """Object for user database entries."""

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(80), unique=True, index=True,
                         nullable=False)
    pw_hash = db.Column('pw_hash', db.String(80), nullable=False)
    phone_number = db.Column('phone_number', db.String(80), nullable=False)
    registered_on = db.Column('registered_on', db.DateTime, nullable=False)

    def __init__(self, username, pw_hash, phone_number):
        """Initialize User object.

        Args:
            username: The username string.
            pw_hash: Password hash value.
            phone_number: User's phone number.
        """
        self.username = username
        self.pw_hash = pw_hash
        self.phone_number = phone_number
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        """Authenticate user."""
        return True

    def is_active(self):
        """Check if user is active."""
        return True

    def is_anonymous(self):
        """Check if user is anonymous."""
        return False

    def get_id(self):
        """Get user Id."""
        return str(self.id)


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


@login_manager.user_loader
def load_user(id):
    """Get the current user's id."""
    return User.query.get(int(id))


@blueprint.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('user.login'))

        # second argument adds remember me cookie
        login_user(registered_user, True)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('user.index'))
    return render_template('login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    """Logout post request."""
    logout_user()
    return redirect('/')


@blueprint.route('/create', methods=['GET', 'POST'])
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
            return redirect(url_for('user.create_account'))

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username, pw_hash, phone_number)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        flash('Successfully created new account for ' + username)
        return redirect(request.args.get('next') or url_for('user.index'))
    return render_template('create_account.html', form=form)


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


@blueprint.route('/markets', methods=['GET', 'POST'])
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


@blueprint.route('/products', methods=['GET', 'POST'])
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
