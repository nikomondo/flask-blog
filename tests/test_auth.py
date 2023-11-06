import pytest
from flask import g, session
from flaskr.db import db
from flaskr.models.auth import User


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    # Check that the second request was to the login page.
    assert b"already registered" not in response.data
    assert b"LogIn" not in response.data
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
