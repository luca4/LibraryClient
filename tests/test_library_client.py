import pytest
from library_client import LibraryClient
from exceptions import *

test_user_not_admin = {"username": "carlo", "password": "bianchi"}
test_user_admin = {"username": "mario", "password": "rossi"}


@pytest.fixture
def client():
    return LibraryClient()


def test_login_success_not_admin(client):
    """Test successful login with non admin user"""

    client.login(test_user_not_admin["username"], test_user_not_admin["password"])

    assert client.auth_token is not None
    assert client.token_expiration > 0
    assert client.is_admin is False


def test_login_success_admin(client):
    """Test successful login with admin user"""

    client.login(test_user_admin["username"], test_user_admin["password"])

    assert client.auth_token is not None
    assert client.token_expiration > 0
    assert client.is_admin is True


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    username = "wrong_user"
    password = "wrong_password"

    with pytest.raises(AuthenticationError):
        client.login(username, password)

    assert client.auth_token is None
    assert client.token_expiration == 0


def test_get_books(client):
    """ Test returning list of books  """
    client.login(test_user_not_admin["username"], test_user_not_admin["password"])
    books = client.get_books()

    assert "books" in books


def test_borrow_book(client):
    """Test borrowing of a book."""
    client.login(test_user_not_admin["username"], test_user_not_admin["password"])

    try:
        client.borrow_book(book_id=1)
    except Exception:
        pytest.fail("borrow_book raised an exception unexpectedly")


def test_return_book(client):
    """Test return of a book."""
    client.login(test_user_not_admin["username"], test_user_not_admin["password"])

    book_id = 1
    client.borrow_book(book_id)

    try:
        client.return_book(book_id)
    except Exception:
        pytest.fail("return_book raised an exception unexpectedly")


def test_add_book_success(client):
    """Test successfully adding a book."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_data = {
        "title": "testTitle",
        "author": "testAuthor",
        "is_borrowed": "false"
    }

    try:
        client.add_book(book_data)
    except Exception:
        pytest.fail("add_book raised an exception unexpectedly")


def test_add_book_invalid_data(client):
    """Test adding a book with invalid data."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_data = {}  # Missing required fields

    with pytest.raises(ValidationError):
        client.add_book(book_data)


def test_delete_book_success(client):
    """Test successfully deleting a book."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_id = 1  # Assumes book ID 1 exists in the mock server

    try:
        client.delete_book(book_id)
    except Exception:
        pytest.fail("delete_book raised an exception unexpectedly")


def test_delete_book_not_found(client):
    """Test deleting a non-existent book."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_id = -1  # Assumes -1 is not valid id

    with pytest.raises(ResourceNotFoundError):
        client.delete_book(book_id)


def test_update_book_success(client):
    """Test successfully updating a book."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_id = 1  # Assumes book ID 1 exists in the mock server
    updated_data = {
        "title": "testTitle2",
        "author": "testAuthor2",
        "is_borrowed": False
    }

    try:
        client.update_book(book_id, updated_data)
    except Exception:
        pytest.fail("update_book raised an exception unexpectedly")


def test_update_book_not_found(client):
    """Test updating a non-existent book."""
    client.login(test_user_admin["username"], test_user_admin["password"])
    book_id = -1  # Assumes -1 is not valid id
    updated_data = {
        "title": "testTitle1",
        "author": "testAuthor1",
        "is_borrowed": True
    }

    with pytest.raises(ResourceNotFoundError):
        client.update_book(book_id, updated_data)
