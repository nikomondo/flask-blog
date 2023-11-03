from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.db import db

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password : Mapped[str] =  mapped_column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"