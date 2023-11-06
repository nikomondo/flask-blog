import os
from flaskr.db import db


def test_testing_config(app):
    assert app.config["TESTING"]
    assert "test.sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]

    

