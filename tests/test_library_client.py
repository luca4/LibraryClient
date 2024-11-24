import pytest
from library_client import LibraryClient


@pytest.fixture
def client():
    return LibraryClient()


def test_login_success_not_admin(client):
    """Test successful login with non admin user"""
    username = "carlo"
    password = "bianchi"

    client.login(username, password)

    assert client.auth_token is not None
    assert client.token_expiration > 0
    assert client.is_admin is False


def test_login_success_admin(client):
    """Test successful login with admin user"""

    client.login("mario", "rossi")

    assert client.auth_token is not None
    assert client.token_expiration > 0
    assert client.is_admin is True


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    username = "wrong_user"
    password = "wrong_password"

    with pytest.raises(Exception) as exc_info:
        client.login(username, password)

    assert str(exc_info.value) == "Wrong username or password"
    assert client.auth_token is None
    assert client.token_expiration == 0
