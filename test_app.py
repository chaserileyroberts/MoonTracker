import flask
import app
import os


test_client = app.app.test_client()


def setup():
    app.WebsiteServer.set_database('test.db')


def teardown():
    os.remove('test.db')


def test_response_elems():
    response = test_client.get('/')
    assert response.status_code == 200
    page = str(response.data)
    assert "Phone Number" in page
    assert "Coin" in page
    assert "Target Price" in page


# TODO(Chase): Add more unit tests
