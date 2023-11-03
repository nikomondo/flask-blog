from sqlalchemy import Integer, String , ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.db import db
from datetime import datetime
from flaskr.models.auth import User

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    created: Mapped[str] = mapped_column(DateTime, unique=True, nullable=False , default=datetime.now())
    liked: Mapped[int] = mapped_column(Integer, nullable=False , default=0)

    def __repr__(self):
        return f'<Post {self.title}>'