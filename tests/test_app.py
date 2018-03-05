from flask import current_app


def test_create_app():
    assert current_app.debug
    assert current_app.testing
