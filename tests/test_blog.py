import pytest
from sqlalchemy import func, select
from flaskr.db import db
from flaskr.models.blog import Post


def test_index(client, auth, insert_user, insert_post):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"j'aime" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth, insert_user, insert_post):
    # change the post author to another user
    with app.app_context():
        post = db.get_or_404(Post, 1)
        post.author_id = 2
        db.session.add(post)
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path, insert_user):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app, insert_user, insert_post):
    auth.login()
    assert client.get("/create").status_code == 200
    response = client.post("/create", data={"title": " titre created", "body": "body"})
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    with app.app_context():
        result = db.session.query(Post).all()
        assert len(result) == 2


def test_update(client, auth, app, insert_user, insert_post):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        post = db.session.query(Post).filter_by(id=1).first()
        assert post.title == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path, insert_user, insert_post):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    print(response.data)
    assert b"Title is required." in response.data


def test_delete(client, auth, app, insert_user, insert_post):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        post = db.session.query(Post).filter_by(id=1).first()
        assert post is None


def test_liking(client, auth, app, insert_user, insert_post):
    auth.login()
    client.get("/1/liking")
    response = client.get("/")
    assert b"bi-hand-thumbs-up-fill" in response.data
    assert b"j'aime" not in response.data

    with app.app_context():
        post = db.session.query(Post).filter_by(id=1).first()
        assert post.liked == 1
