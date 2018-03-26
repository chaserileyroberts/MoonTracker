from moontracker.models import Alert
from tests.utils import test_client


def test_valid_post():
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


def test_valid_post_below():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='0',
            target_price='100',
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
    assert 'Field must be at least 10 characters long' in str(response.data)

    results = Alert.query.filter().all()
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
    assert 'Input characters must be numeric' in str(response.data)

    results = Alert.query.filter().all()
    assert len(results) == 0


def test_nonint_price():
    response = test_client.post(
        '/',
        data=dict(
            phone_number='5558675309',
            asset='BTC',
            less_more='1',
            target_price='aaaaa'
        ))
    assert response.status_code == 200
    assert 'Not a valid integer value' in str(response.data)

    results = Alert.query.filter().all()
    assert len(results) == 0


def test_product_page():
    response = test_client.post(
        '/products',
        data=dict(
            phone_number='5558675309',
            product='BTC',
            less_more='1',
            target_price='100',
            market='coinbase'
        ))
    assert response.status_code == 200
    assert 'Alert is set!' in str(response.data)
    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC',
                                 Alert.price == 100.0,
                                 Alert.above == 1,
                                 Alert.market == 'coinbase').all()
    assert len(results) == 1
