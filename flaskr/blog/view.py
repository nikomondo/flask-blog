from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth.view import login_required
from flaskr.db import db
from flaskr.blog.model import Post
from flaskr.auth.model import User

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    posts = db.session.query(Post, User).join(User, Post.author_id == User.id).all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    post = db.get_or_404(
        Post, id, description="Post id {id} doesn't exist.".format(id=id)
    )

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/details", methods=("GET",))
@login_required
def details(id):
    post = db.get_or_404(Post, id)
    return render_template("blog/details.html", post=post)


@bp.route("/<int:id>/liking", methods=("GET",))
@login_required
def liking(id):
    post = db.get_or_404(Post, id)
    if post.liked == 0:
        post.liked = 1
    else:
        post.liked = 0
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("blog.index"))
