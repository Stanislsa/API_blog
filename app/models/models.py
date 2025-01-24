from sqlalchemy import Column, BigInteger, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    categorie_id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    name = Column(Text, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    posts = relationship("Post", back_populates="category")


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    username = Column(Text, nullable=False, unique=True)

    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="NO ACTION", onupdate="NO ACTION"), nullable=False)
    categorie_id = Column(BigInteger, ForeignKey("categories.categorie_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    title = Column(Text)
    content = Column(Text)
    status = Column(Text, nullable=False)
    published_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
