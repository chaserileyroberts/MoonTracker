from moontracker.models import User


def test_sanity():
    user = User("test", "test", "1111111111")

    assert user.is_authenticated()
    assert user.is_active()
    assert not user.is_anonymous()
