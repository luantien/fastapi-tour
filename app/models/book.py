from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from models import AuthorViewModel, UserBaseModel
from schemas import BookMode


class SearchBookModel():
    def __init__(self, title, author_id, page, size) -> None:
        self.title = title
        self.author_id = author_id
        self.page = page
        self.size = size

class BookModel(BaseModel):
    title: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    author_id: UUID
    mode: BookMode = Field(default=BookMode.DRAFT)
    owner_id: Optional[UUID] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Book 1",
                "description": "Description for Book 1",
                "rating": 4,
                "author_id": "123e4567-e89b-12d3-a456-426614174000",
                "mode": "DRAFT"
            }
        }

class BookViewModel(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    rating: int
    author_id: UUID
    author: AuthorViewModel
    owner_id: UUID | None = None
    owner: UserBaseModel | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
