from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from wtforms import (Form, StringField, IntegerField,
                     SelectField, validators)
from texter import Texter
from flask_wtf import RecaptchaField, Recaptcha
import json
import sys
from assets import assets
from flask_login import LoginManager, login_user, logout_user, login_required


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JOBS = [
        {
            'id': 'job1',
            'func': 'app:check_alerts',
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    SCHEDULER_API_ENABLED = True
    SECRET_KEY = "0"  # Not a big deal for now


app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'secret123'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
app.config['RECAPTCHA_PRIVATE_KEY'] = (
    '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
db = SQLAlchemy(app)
texter = Texter()
login = LoginManager(app)


class AlertForm(Form):
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
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    above = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)


def check_alerts():
    with app.app_context():
        texter.check_alerts(db)


@app.route('/', methods=['GET', 'POST'])
def index():
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
    # to do: connect to database properly
    __tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(80), unique=True, index=True, nullable=False)
    password = db.Column('password', db.String(80), nullable=False)
    phone_number = db.Column('phone_number', db.String(80), nullable=False)

    def __init__(self, username, password, phone_number, active=True):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.active = active
        self.id = 1  # for now

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        # return unicode(self.session_token)
        return str(self.id) # python2 uses unicode()


class LoginForm(Form):
    username = StringField('Username', [
            validators.Length(
                min=1, message="Please enter username")])
    password = StringField('Password', [
            validators.Length(min=8, message="Please enter password")])


class NewAccountForm(Form):
    username = StringField('Username', [
            validators.Length(
                min=1, message="Please enter username")]) # query to see if username is in use
    password = StringField('Password', [
            validators.Length(
                min=8, message="Password must be at least 8 characters")])
    phone_number = StringField(
        'Phone Number', [
            validators.Length(
                min=10), validators.Regexp(
                '^[0-9]+$', message="Input characters must be numeric")])


#for testing
user = User('s', '123', '111')

@login.user_loader
def load_user(session_token):
    # return User.query.filter_by(session_token=session_token).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate(): # validate should be customized I think
        # to do: login user
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        # to do: check if url is safe
        return redirect(next or '/')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    form = NewAccountForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data, form.phone_number.data)
        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        # to do: check if url is safe
        return redirect(next or '/')
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


@app.route('/markets', methods=['GET', 'POST'])
def route_markets():
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


@app.route('/products', methods=['GET', 'POST'])
def route_products():
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


if __name__ == '__main__':
    texter.set_clients()
    port = 8080
    if len(sys.argv) == 2 and sys.argv[1] == '--live':
        from api_keys import recaptcha_public, recaptcha_private
        app.config['RECAPTCHA_PUBLIC_KEY'] = recaptcha_public
        app.config['RECAPTCHA_PRIVATE_KEY'] = recaptcha_private
    db.create_all()
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=port)
