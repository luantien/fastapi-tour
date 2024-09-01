import enum
from database import Base
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity


class BookMode(enum.Enum):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'

class OwnerSource(enum.Enum):
    COGNITO = 'COGNITO'
    LOCAL = 'LOCAL'

class Book(BaseEntity, Base):
    __tablename__ = "books"

    title = Column(String)
    description = Column(String)
    mode = Column(Enum(BookMode), nullable=False, default=BookMode.DRAFT)
    rating = Column(SmallInteger, nullable=False, default=0)
    author_id = Column(Uuid, ForeignKey("authors.id"), nullable=False)
    owner_id = Column(Uuid, nullable=True)
    owner_source = Column(Enum(OwnerSource), nullable=False, default=OwnerSource.LOCAL)

    author = relationship("Author")
