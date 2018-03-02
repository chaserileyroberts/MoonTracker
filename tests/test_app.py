from flask import current_app
from moontracker.app import Alert

test_client = current_app.test_client()


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
            target_price='100',
        ))
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)
    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.above).all()

    assert len(results) == 1


def test_post_to_db_below():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='0',
            target_price='100'
        ))
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)
    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.above == 0).all()

    assert len(results) == 1


def test_short_phonenumber():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='3',
            asset='BTC',
            less_more='1',
            target_price='100'
        ))
    assert response.status_code == 200
    page = str(response.data)
    assert 'Field must be at least 10 characters long' in page
    results = Alert.query.filter(Alert.phone_number == '3',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.above).all()
    assert len(results) == 0


def test_nonint_phonenumber():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='aaaaa',
            asset='BTC',
            less_more='1',
            target_price='100'
        ))
    assert response.status_code == 200
    page = str(response.data)
    assert 'Input characters must be numeric' in page
    results = Alert.query.filter(Alert.phone_number == 'aaaaa',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.above).all()
    assert len(results) == 0


def test_post_to_db_bad_price():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='1',
            target_price='aaaaa'
        ))
    assert response.status_code == 200
    page = str(response.data)
    assert 'Not a valid integer value' in page
    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC', Alert.price == 'aaaaa',
                                 Alert.above).all()
    assert len(results) == 0
