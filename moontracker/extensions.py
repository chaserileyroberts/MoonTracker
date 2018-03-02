"""Extensions module."""

from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


scheduler = APScheduler()
bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
