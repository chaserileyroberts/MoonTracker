from moontracker.models import Alert
from tests.utils import register, test_client

from moontracker.extensions import db


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
    assert 'LTC' in str(response.data)
    assert '$100.00' in str(response.data)
    assert '1111111111' in str(response.data)

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='BTC',
            less_more='0',
            target_price='50',
            # user_id = '1'  # fake user id
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 2

    response = test_client.get('/manage', follow_redirects=True)
    assert 'BTC' in str(response.data)
    assert '$50.00' in str(response.data)
    assert '1111111111' in str(response.data)


def test_delete_db_updates_display():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            less_more='1',
            target_price='500',
            # user_id = '1'  # fake user id
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    db.session.delete(results[0])
    db.session.commit()

    response = test_client.get('/manage', follow_redirects=True)
    assert '$500.00' not in str(response.data)
    assert '1111111111' not in str(response.data)


def test_update_db_updates_display():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200

    response = test_client.post(
        '/',
        data=dict(
            phone_number='1111111111',
            asset='LTC',
            less_more='1',
            target_price='500',
            # user_id = '1'  # fake user id
        ))
    assert response.status_code == 200

    results = Alert.query.filter(Alert.user_id == 1).all()
    assert len(results) == 1

    results[0].price = 4000.0
    db.session.merge(results[0])
    db.session.commit()

    response = test_client.get('/manage', follow_redirects=True)
    assert '$4000.00' in str(response.data)
    assert '$500.00' not in str(response.data)
    assert '1111111111' in str(response.data)

    results[0].sybmol = 'BTC'
    db.session.merge(results[0])
    db.session.commit()

    response = test_client.get('/manage', follow_redirects=True)
    assert 'BTC' in str(response.data)
    assert '$4000.00' in str(response.data)
    assert '$500.00' not in str(response.data)
    assert '1111111111' in str(response.data)


def delete_button():
    # I believe this requires front-end testing

    # response = test_client.post(
    #     '/manage',
    #     data=dict(

    #     ))

    pass


def update_button():
    # I believe this requires front-end testing
    pass
