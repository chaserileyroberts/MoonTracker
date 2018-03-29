"""Flask Config module."""

import os


class Config(object):
    """Base configuration for the flask app."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JOBS = [
        {
            'id': 'job1',
            'func': 'moontracker.app:check_alerts',
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True
    SECRET_KEY = os.urandom(256)

    DEBUG = False
    TESTING = False

    def set_recaptcha_keys():
        """Set the default recaptcha keys."""
        Config.RECAPTCHA_PUBLIC_KEY = (
            '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
        Config.RECAPTCHA_PRIVATE_KEY = (
            '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')


class DevConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'

    DEBUG = True


class ProdConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'

    def set_recaptcha_keys():
        """Import and sets the production recaptcha keys."""
        from moontracker.api_keys import recaptcha_public, recaptcha_private
        ProdConfig.RECAPTCHA_PUBLIC_KEY = recaptcha_public
        ProdConfig.RECAPTCHA_PRIVATE_KEY = recaptcha_private


class TestConfig(Config):
    """Development configuration."""

    # Test API_keys.
    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    JOBS = []
    DEBUG = True
    TESTING = True

    # Allows for marginally faster tests, at the cost of security
    # (default is 12, minimum is 4)
    BCRYPT_LOG_ROUNDS = 4
