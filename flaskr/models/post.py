from sqlalchemy import Integer, String , ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    created: Mapped[str] = mapped_column(DateTime, unique=True, nullable=False)
    liked: Mapped[int] = mapped_column(Integer, nullable=False , default=0)