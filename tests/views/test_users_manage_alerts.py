from moontracker.models import Alert
from tests.utils import register, test_client


def test_correct_num_alerts():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data={
            'phone_number': '1111111111',
            'asset': 'LTC',
            'market': 'coinbase',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert "No alerts" not in str(response.data)
    assert 'Litecoin' in str(response.data)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)


def test_edit():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data={
            'phone_number': '1111111111',
            'asset': 'LTC',
            'market': 'gdax',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)
    response = test_client.post(
        '/manage',
        data={
            'alert_id': str(results[0].id),
            'phone_number': '1111111111',
            'asset': 'BTC',
            'market': 'gdax',
            'price': '20',
            'cond_option': '1',
            'submit': 'Save Changes'
        })
    assert response.status_code == 200
    response = test_client.get('/manage', follow_redirects=True)
    assert '$20' in str(response.data)
    assert '$100' not in str(response.data)


def test_delete():
    response = register('test_user', '12345678', '1111111111')
    assert 'test_user' in str(response.data)
    assert response.status_code == 200
    response = test_client.post(
        '/',
        data={
            'phone_number': '1111111111',
            'asset': 'LTC',
            'market': 'gemini',
            'cond_option': '1',
            'price': '100'
        })
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)
    response = test_client.post(
        data={
            'alert_id': str(results[0].id),
            'phone_number': '1111111111',
            'asset': 'LTC',
            'cond_option': '1',
            'price': '100',
            'submit': 'Delete'
        })
    assert response.status_code == 200
    response = test_client.get('/manage', follow_redirects=True)
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 0
    assert "$100" not in str(response.data)

    response = test_client.post(
        '/',
        data={
            'phone_number': '1111111111',
            'asset': 'BTC',
            'market': 'gemini',
            'cond_option': '0',
            'price': '50'
        })
    assert "test_user" in str(response.data)
    assert response.status_code == 200
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '$50.00' in str(response.data)
    assert '1111111111' in str(response.data)


def test_add():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    response = test_client.get('/manage', follow_redirects=True)
    assert "No alerts" in str(response.data)
    response = test_client.post(
        '/manage',
        data={
            'alert_id': '-1',
            'phone_number': '1111111111',
            'asset': 'LTC',
            'market': 'coinbase',
            'cond_option': '1',
            'price': '825',
            'submit': 'Save Changes'
        })
    print(response.data)
    response = test_client.get('/manage', follow_redirects=True)
    assert "No alerts" not in str(response.data)
    assert "$825.00" in str(response.data)
    assert "above" in str(response.data)
