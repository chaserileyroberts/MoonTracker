"""Flask Config module."""


class Config(object):
    """Base configuration for the flask app."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JOBS = [
        {
            'id': 'job1',
            'func': 'moontracker.app:check_alerts',
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    SCHEDULER_API_ENABLED = True
    SECRET_KEY = "0"  # Not a big deal for now

    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Development configuration."""

    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'

    DEBUG = True


class ProdConfig(Config):
    """Production configuration."""

    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///moontracker_database.db'


class TestConfig(Config):
    """Development configuration."""

    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'

    DEBUG = True
    TESTING = True

    # Allows for marginally faster tests, at the cost of security
    # (default is 12, minimum is 4)
    BCRYPT_LOG_ROUNDS = 4
