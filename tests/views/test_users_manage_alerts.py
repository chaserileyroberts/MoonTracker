from moontracker.models import Alert
from tests.utils import register, test_client
# from flask_login import current_user


def test_correct_num_alerts():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            less_more='1',
            target_price='100',
            # user_id = '1'  # fake user id
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
            less_more='1',
            target_price='100',
            # user_id = '1'  # fake user id
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '<b>Asset:</b> Litecoin' in str(response.data)
    assert '$100' in str(response.data)
    assert '1111111111' in str(response.data)
    response = test_client.post('/manage', 
        data=dict(
            phone_number="1111111111",
            asset="BTC",
            less_more="1",
            target_price="100",
            alert_id='1',
            submit="Save Changes"
        ),
        follow_redirects=True)
    assert response.status_code == 200   
    response = test_client.get('/manage', follow_redirects=True)
    assert '<b>Asset:</b> Bitcoin' in str(response.data)
    assert '<b>Asset:</b> Litcoin' not in str(response.data)


def test_delete():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            less_more='1',
            target_price='100',
            # user_id = '1'  # fake user id
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    response = test_client.get('/manage', follow_redirects=True)
    assert '<b>Asset:</b> Litecoin' in str(response.data)
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
    assert '<b>Asset:</b> Litcoin' not in str(response.data)
    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 0