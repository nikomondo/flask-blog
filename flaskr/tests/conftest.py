from typing import Any
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from flaskr import create_app
from flaskr.db import db


@pytest.fixture()
def app():
    app = create_app(test=True)
    app.config.update(TESTING=True, DEBUG=True)

    # other setup can go here
    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()
        db.session.remove()


@pytest.fixture
def client(app: Any):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client: Any):
    return AuthActions(client)


@pytest.fixture
def insert_user(app: Any):
    from flaskr.auth.model import User

    test_pwd = generate_password_hash("test")
    other_pwd = generate_password_hash("other")

    with app.app_context():
        user1 = User(
            username="test",
            password=test_pwd,
        )
        user2 = User(
            username="other",
            password=other_pwd,
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()


@pytest.fixture()
def insert_post(app: Any):
    from flaskr.blog.model import Post

    date = datetime(2018, 1, 1)
    with app.app_context():
        post = Post(
            title="test title",
            body="test body",
            author_id=1,
            created=date,
            liked=0,
        )
        db.session.add(post)
        db.session.commit()