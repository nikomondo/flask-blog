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

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # initialize the app with the extension
    from flaskr.db import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from flaskr.auth import view

    app.register_blueprint(view.bp)

    from flaskr.blog import view

    app.register_blueprint(view.bp)
    app.add_url_rule("/", endpoint="index")


    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app

app = create_app(test=True)