import pytest
from flask import g, session
from flaskr.db import db
from flaskr.auth.model import User


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    # Check that the second request was to the login page.
    assert b"already registered" not in response.data
    assert b"<h1>Log In</h1>" not in response.data
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert db.one_or_404(db.select(User).filter_by(username="a")) is not None


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message, insert_user):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert response.request.path == "/auth/register"
    assert response.status_code == 200
    assert message in response.data


def test_login(client, auth, insert_user):
    assert client.get("/auth/login").status_code == 200
    # response = auth.login()
    response = client.post("/auth/login", data={"username": "test", "password": "test"})
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session.get("user_id") == 1
        assert g.user.username == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"User a is not registered."),
        ("test", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, username, password, message, insert_user):
    response = auth.login(username, password)
    assert message in response.data
