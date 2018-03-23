from moontracker.models import Alert
from tests.utils import register, login, logout, test_client
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
	assert 'LTC' in str(response.data)
	assert '$100' in str(response.data)
	assert '1111111111' in str(response.data)

	# assert 'BTC' not in str(response.data)
