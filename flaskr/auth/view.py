import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import exc, select
from flaskr.db import db
from flaskr.auth.model import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

#regex=r'^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*[A-Z])(?=.*\d).{4,20}$',
#message="Le mot de passe doit contenir au moins un caractère spécial, une majuscule, un chiffre, et avoir une longueur entre 4 et 20 caractères."
class RegisterForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25) , DataRequired()])
    password = PasswordField('New Password', [ DataRequired(), EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_or_404(User, user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and  form.validate_on_submit():
            try:
                user = User(
                    username=form.username.data, password=generate_password_hash(form.password.data)
                )
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash( f"User {form.username.data} is already registered.")
            else:
                return redirect(url_for("auth.login"))

    return render_template("auth/register.html" , form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = db.session.query(User).filter_by(username=username).first()

        if user is None:
            error = f"User {username} is not registered."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
