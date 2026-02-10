from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    author: Mapped[list["Comment"]] = relationship( back_populates="author")
    user: Mapped[list["Post"]] = relationship( back_populates="user")
    """ user_from: Mapped[list["Follower"]] = relationship( back_populates="user_from")
    user_to: Mapped[list["Follower"]] = relationship( back_populates="user_to") """
    user_from: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.user_from_id",
        back_populates="user_from"
    )

    user_to: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.user_to_id",
        back_populates="user_to"
    )

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text())
    autor_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    author: Mapped["User"] = relationship( back_populates="author")
    post: Mapped["Post"] = relationship( back_populates="post")

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post: Mapped[list["Comment"]] = relationship( back_populates="post")
    user: Mapped["User"] = relationship( back_populates="user")
    media: Mapped[list["Media"]] = relationship( back_populates="media")

class Media(db.Model):
    __tablename__ = "Media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType, native_enum=False),nullable=False )
    url: Mapped[str] = mapped_column(String(120), unique=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    media: Mapped["Post"] = relationship( back_populates="media")

class Follower(db.Model):
    __tablename__ = "follower"
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    """ user_from: Mapped["User"] = relationship( back_populates="user_from")
    user_to: Mapped["User"] = relationship( back_populates="user_to") """
    user_from: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id],
        back_populates="user_from"
    )

    user_to: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="user_to"
    )

