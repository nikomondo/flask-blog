import pytest
import os
import tempfile
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
def client(app):
    return app.test_client()


@pytest.fixture
def insert_user(app):
    from flaskr.models.auth import User

    with app.app_context():
        user1 = User(
            username="test",
            password="'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'",
        )
        user2 = User(
            username="other",
            password="pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79",
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()


@pytest.fixture()
def insert_post():
    from flaskr.models.blog import Post

    with app.app_context():
        post = Post(
            title="test title",
            body="test body",
            author_id=1,
            created="2018-01-01 00:00:00",
            liked=0,
        )
        db.session.add(post)
        db.session.commit()
