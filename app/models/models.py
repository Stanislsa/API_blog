from sqlalchemy import Column, DateTime
from datetime import datetime
from sqlalchemy import Column, BigInteger, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    categorie_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    name = Column(Text, nullable=False, unique=True)

    posts = relationship("Post", back_populates="category")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text)
    is_admin = Column(Boolean, nullable=False, default=False)
    username = Column(Text, nullable=False, unique=True)

    posts = relationship("Post", back_populates="user")


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    post_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="NO ACTION", onupdate="NO ACTION"), nullable=False)
    categorie_id = Column(BigInteger, ForeignKey("categories.categorie_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    title = Column(Text)
    content = Column(Text)
    status = Column(Text, nullable=False)
    published_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")