from flask import current_app

test_client = current_app.test_client()


def register(username, password, phone_number):
    return test_client.post('/create', data=dict(
        username=username,
        password=password,
        phone_number=phone_number
    ), follow_redirects=True)


def login(username, password):
    return test_client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)


def logout():
    return test_client.get('/logout', follow_redirects=True)


def test_create_login_logout():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)
    response = login('test_user', '12345678')
    assert response.status_code == 200
    assert 'Logged in successfully' in str(response.data)
    response = logout()
    assert response.status_code == 200


def test_create_duplicate_user():
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Successfully created new account for test_user' in str(
        response.data)
    response = logout()
    assert response.status_code == 200
    response = register('test_user', '12345678', '1111111111')
    assert response.status_code == 200
    assert 'Username not available' in str(response.data)


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

# TO DO: test database
