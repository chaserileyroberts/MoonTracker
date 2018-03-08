"""Module for creating the Flask app.

More information provided in the create_app() docstring.
"""
from flask import Flask

from moontracker.extensions import scheduler, bcrypt, login_manager, db
from moontracker.extensions import socketio
from moontracker.last_prices import broadcast_last_prices
from moontracker.texter import Texter
from moontracker.views.home.views import home_blueprint
from moontracker.views.users.views import users_blueprint


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
    socketio.init_app(app)

    def datetimefmt(dt):
        return dt.strftime('%c')

    app.jinja_env.filters['datetimefmt'] = datetimefmt


def register_blueprints(app):
    """Register all blueprints to the Flask application."""
    app.register_blueprint(home_blueprint)
    app.register_blueprint(users_blueprint)


def check_alerts():
    """Check for alerts on the database."""
    with db.app.app_context():
        texter.check_alerts()
        broadcast_last_prices()
