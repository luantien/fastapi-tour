import uuid
from database import Base
from sqlalchemy import Column, String, Uuid, Enum
from sqlalchemy.orm import relationship
from schemas.base_entity import BaseEntity, Gender

class Author(BaseEntity, Base):
    __tablename__ = "authors"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    gender = Column(Enum(Gender), nullable=False, default=Gender.NONE)

    books = relationship("Book", back_populates="author")
