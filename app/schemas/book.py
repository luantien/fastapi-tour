import enum
import uuid
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum, Table
from sqlalchemy.orm import relationship
from database import Base, metadata
from .base_entity import BaseEntity


class BookMode(enum.Enum):
    DRAFT = 'D'
    PUBLISHED = 'P'


class Book(Base, BaseEntity):
    __tablename__ = "books"

    title = Column(String)
    description = Column(String)
    mode = Column(Enum(BookMode), nullable=False, default=BookMode.DRAFT)
    rating = Column(SmallInteger, nullable=False, default=0)
    author_id = Column(Uuid, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
