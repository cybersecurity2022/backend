import uuid

from sqlalchemy import Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String(32), primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    hash_password = Column(String(512), nullable=False)

    store = relationship("Store", backref="user", cascade="all, delete-orphan", uselist=False)

    __table_args__ = (UniqueConstraint('email'), UniqueConstraint('user_name'),)

    def __init__(self, user_name, email, hash_password):
        self.id = str(uuid.uuid4().hex)
        self.user_name = user_name
        self.email = email
        self.hash_password = hash_password


class Store(Base):
    __tablename__ = "stores"
    id = Column(String(32), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)

    user_id = Column(String(32), ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint('title'),)

    def __init__(self, title, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.description = description

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
