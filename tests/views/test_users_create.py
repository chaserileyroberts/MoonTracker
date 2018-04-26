from tests.utils import register, logout


def test_create_user():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)


def test_create_duplicate_user():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    response = logout()
    assert response.status_code == 200
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Username not available' in str(response.data)


def test_empty_username():
    response = register('', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Please enter username' in str(response.data)


def test_short_password():
    response = register('test_user', '12345', '1111111111')
    assert response.status_code == 200
    assert 'Password must be at least 8 characters' in str(response.data)


def test_short_phonenumber():
    response = register('test_user', '12345678', '11111111')
    assert response.status_code == 200
    assert 'Please enter a valid phone number' in str(response.data)


def test_nonint_phonenumber():
    response = register('test_user', '12345678', 'aaaaaaaaaa')
    assert response.status_code == 200
    assert 'Input characters must be numeric' in str(response.data)
