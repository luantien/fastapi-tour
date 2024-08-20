import enum
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity


class BookMode(enum.Enum):
    DRAFT = 'D'
    PUBLISHED = 'P'


class Book(BaseEntity, Base):
    __tablename__ = "books"

    title = Column(String)
    description = Column(String)
    mode = Column(Enum(BookMode), nullable=False, default=BookMode.DRAFT)
    rating = Column(SmallInteger, nullable=False, default=0)
    author_id = Column(Uuid, ForeignKey("authors.id"), nullable=False)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=True)

    author = relationship("Author")
    owner = relationship("User")
