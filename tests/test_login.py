from app import User, db, app
import app as webserver

# This is very much not working because I'm
# having testing issues

def setup():
	test_client = app.test_client()
	app.testing = True
	db.drop_all()
	db.create_all()

def teardown():
	db.drop_all()

def test_login():
	user = User('test_user', '', '12345678')