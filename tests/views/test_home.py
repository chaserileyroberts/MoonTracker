from moontracker.models import Alert
from tests.utils import test_client


def test_valid_post():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'gemini',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)

    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.condition).all()
    assert len(results) == 1


def test_percent_above():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'bitfinex',
            'cond_option': '2',
            'percent': '100',
            'percent_duration': '86400'
        })
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)
    results = Alert.query.filter(
        Alert.phone_number == '5558675309',
        Alert.symbol == 'BTC',
        Alert.percent == 100.0,
        Alert.condition == 2,
        Alert.percent_duration).all()
    assert len(results) == 1


def test_percent_below():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'bitfinex',
            'cond_option': '3',
            'percent': '100',
            'percent_duration': '86400'
        })
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)
    results = Alert.query.filter(
        Alert.phone_number == '5558675309',
        Alert.symbol == 'BTC',
        Alert.percent == 100.0,
        Alert.condition == 3,
        Alert.percent_duration).all()
    assert len(results) == 1


def test_valid_post_below():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'bitfinex',
            'cond_option': '0',
            'price': '100'
        })
    assert response.status_code == 200
    assert "Please do the recaptcha" not in str(response.data)

    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC', Alert.price == 100.0,
                                 Alert.condition == 0).all()
    assert len(results) == 1


def test_short_phonenumber():
    response = test_client.post(
        '/',
        data={
            'phone_number': '3',
            'asset': 'BTC',
            'market': 'gemini',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200
    assert 'Field must be at least 10 characters long' in str(response.data)

    results = Alert.query.filter().all()
    assert len(results) == 0


def test_nonint_phonenumber():
    response = test_client.post(
        '/',
        data={
            'phone_number': 'aaaaa',
            'asset': 'BTC',
            'market': 'gemini',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200
    assert 'Input characters must be numeric' in str(response.data)

    results = Alert.query.filter().all()
    assert len(results) == 0


def test_nonint_price():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'gdax',
            'cond_option': '1',
            'price': 'aaaaa'
        })
    assert response.status_code == 200
    assert 'Not a valid float value' in str(response.data)

    results = Alert.query.filter().all()
    assert len(results) == 0


def test_product_page():
    response = test_client.post(
        '/',
        data={
            'phone_number': '5558675309',
            'asset': 'BTC',
            'market': 'coinbase',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200
    assert 'Alert is set!' in str(response.data)
    results = Alert.query.filter(Alert.phone_number == '5558675309',
                                 Alert.symbol == 'BTC',
                                 Alert.price == 100.0,
                                 Alert.condition == 1,
                                 Alert.market == 'coinbase').all()
    assert len(results) == 1
