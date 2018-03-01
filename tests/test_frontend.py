from app import db, app


def setup():
    app.testing = True
    db.drop_all()
    db.create_all()


def teardown():
    db.drop_all()
