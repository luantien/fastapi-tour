from sqlalchemy import Column, Uuid, Time
from enum import Enum
import uuid

class Gender(Enum):
    NONE = 'N'
    FEMALE = 'F'
    MALE = 'M'


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)
