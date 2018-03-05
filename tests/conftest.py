"""Contains test directory specific hooks."""
import pytest

from moontracker.app import create_app
from moontracker.config import TestConfig
from moontracker.extensions import db


@pytest.fixture(scope='session', autouse=True)
def db_session():
    """Drop the database before the session starts, and create_all at the end.

    The reason behind this is that the scheduler sometimes runs immediately
    following all tests, so we want an empty schema in place so it doesn't
    throw an error. Then when the next test session runs, we drop_all so
    there's no vestigial data leftover from the last session.
    """
    db.drop_all()
    yield
    db.create_all()


@pytest.fixture(scope='function', autouse=True)
def db_function():
    """Create and drop the database before and after each test."""
    db.create_all()
    yield
    db.drop_all()


# Create app and push the application context, so the tests can access
# the app with current_app
create_app(TestConfig).app_context().push()
