from tests.utils import register, logout, login
from tests.utils import test_client
from moontracker.models import User

def test_change_password():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)
    response = login('test_user', '12345678')
    assert response.status_code == 200
    response = test_client.get(
        '/settings',
        follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post(
        '/settings',
		data=dict(
			current_password='12345678',
			new_password='dankmemes',
			new_password_check='dankmemes',
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert "Successfully changed password" in str(response.data)
    response =  logout()
    assert response.status_code == 200
    assert 'test_user' not in str(response.data)
    response = login('test_user', '12345678')
    assert response.status_code == 200
    assert 'test_user' not in str(response.data)
    response = login('test_user', 'dankmemes')
    assert response.status_code == 200
    assert 'test_user' in str(response.data)

def test_bad_password():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)
    response = login('test_user', '12345678')
    assert response.status_code == 200
    response = test_client.get(
        '/settings',
        follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post(
        '/settings',
		data=dict(
			current_password='thisisbad',
			new_password='dankmemes',
			new_password_check='dankmemes',
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert "Current password is invalid" in str(response.data)

def test_mismatched_passwords():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)
    response = login('test_user', '12345678')
    assert response.status_code == 200
    response = test_client.get(
        '/settings',
        follow_redirects=True)
    assert response.status_code == 200
    response = test_client.post(
        '/settings',
		data=dict(
			current_password='12345678',
			new_password='dankmemes',
			new_password_check='surrealmemes',
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert "New passwords do not match" in str(response.data)
