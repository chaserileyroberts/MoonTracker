from moontracker.models import Alert
from tests.utils import register, test_client


def test_correct_num_alerts():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            market='coinbase',
            less_more='1',
            target_price='100',
        ))
    assert response.status_code == 200
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert 'Litecoin' in str(response.data)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)


def test_edit():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            market='gdax',
            less_more='1',
            target_price='100',
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)
    response = test_client.post('/manage',
                                data=dict(
                                    phone_number="1111111111",
                                    asset="BTC",
                                    less_more="1",
                                    target_price="20",
                                    alert_id='1',
                                    submit="Save Changes"
                                ),
                                follow_redirects=True)
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
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            market='gemini',
            less_more='1',
            target_price='100',
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)
    response = test_client.post('/manage',
                                data=dict(
                                    phone_number="1111111111",
                                    asset="LTC",
                                    less_more="1",
                                    target_price="100",
                                    alert_id='1',
                                    submit="Delete"
                                ),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/manage', follow_redirects=True)
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 0
    assert "$100" not in str(response.data)

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='BTC',
            less_more='0',
            market='gemini',
            target_price='50',
        ))
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
        data=dict(
            phone_number="1111111111",
            asset="LTC",
            less_more="1",
            target_price="825",
            alert_id='-1',
            submit="Save Changes"
        ),
        follow_redirects=True)
    print(response.data)
    assert "No alerts" not in str(response.data)
    assert "$825" in str(response.data)
    assert "above" in str(response.data)
