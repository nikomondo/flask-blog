import os
from flask import Flask


def create_app(test=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test:
        DATABASE_URI = "sqlite:///" + os.path.join(app.instance_path, "test.sqlite")
    else:
        DATABASE_URI = "sqlite:///" + os.path.join(app.instance_path, "flaskr.sqlite")


    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or "dev",
        SQLALCHEMY_DATABASE_URI=DATABASE_URI,
    )

    # initialize the app with the extension
    from flaskr.db import db

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
