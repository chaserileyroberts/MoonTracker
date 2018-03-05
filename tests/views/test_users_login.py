from tests.utils import register, login, logout


def test_login_logout():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    response = login('test_user', '12345678')
    assert response.status_code == 200
    assert 'Logged in successfully' in str(response.data)
    response = logout()
    assert response.status_code == 200


def test_empty_username():
    response = login('', '12345678')
    assert response.status_code == 200
    assert 'Please enter username' in str(response.data)


def test_empty_password():
    response = login('test_user', '')
    assert response.status_code == 200
    assert 'Please enter password' in str(response.data)


def test_invalid_account():
    response = login('test_user', '12345678')
    assert response.status_code == 200
    assert 'Username or Password is invalid' in str(response.data)
