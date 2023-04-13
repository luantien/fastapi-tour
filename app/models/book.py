from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from models import AuthorViewModel
from schemas import BookMode


class SearchBookModel(BaseModel):
    title: Optional[str]
    author_id: Optional[UUID]
    page: int = Field(gt=0, default=1)
    size: int = Field(gt=0, le=50, default=10)

class BookModel(BaseModel):
    title: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    author_id: UUID
    mode: BookMode = Field(default=BookMode.DRAFT)

class BookViewModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    rating: int
    author_id: UUID
    author: AuthorViewModel
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
