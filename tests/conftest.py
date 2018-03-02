"""Contains directory specific hooks."""
import pytest

from moontracker.app import create_app
from moontracker.config import TestConfig
from moontracker.extensions import db


@pytest.fixture(scope='function', autouse=True)
def db_session():
    """Create and drop the database before and after each test."""
    db.create_all()
    yield
    db.drop_all()


create_app(TestConfig).app_context().push()
