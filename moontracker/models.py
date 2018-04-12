"""Models used for the SQLAlchemy database."""
from datetime import datetime

from moontracker.extensions import db


class Alert(db.Model):
    """Object to add to database."""

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    above = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    market = db.Column(db.String)
    end_date = db.Column(db.DateTime)


class User(db.Model):
    """Object for user database entries."""

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True,
                         nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

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

    def set_password(self, pw_hash):
        """Set password to a specified hash."""
        self.pw_hash = pw_hash


class LastPrice(db.Model):
    """Object for the last price."""

    symbol = db.Column(db.String(80), primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime)
