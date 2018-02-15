import flask
import app
import os
import sqlite3
import time
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


def test_post_to_db():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='1',
            target_price='100'
        ))
    assert response.status_code == 200
    db_connection = sqlite3.connect('test.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        'SELECT phone_number, price, symbol, above FROM alerts')
    results = db_cursor.fetchall()
    print(results)
    assert len(results) == 1
    assert results[0] == ('5558675309', 100.0, "BTC", 1)

# def test_invalid_form_input_phone():
#     response = test_client.post(
#         '/',
#         data=dict(
#             phone_number='aaaaa',
#             asset='BTC',
#             less_more='1',
#             target_price='100'
#         ))
#     assert response.status_code == 200

# def test_invalid_form_input_price():
#     response = test_client.post(
#         '/',
#         data=dict(
#             phone_number='111111111',
#             asset='BTC',
#             less_more='1',
#             target_price='aaaaa'
#         ))
#     assert response.status_code == 200
#     # assert response.validate
