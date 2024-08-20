from pydantic import BaseModel, Field
from schemas.base_entity import Gender
from datetime import datetime
from uuid import UUID

class AuthorModel(BaseModel):
    full_name: str = Field(min_length=2)
    gender: Gender = Field(default=Gender.NONE)


class AuthorViewModel(BaseModel):
    id: UUID 
    full_name: str
    gender: Gender
    created_at: datetime | None = None
    
    class Config:
        from_attributes = True
