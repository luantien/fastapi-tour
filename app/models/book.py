from typing import Optional
from pydantic import BaseModel, Field


class SearchBookModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    page: int = Field(gt=0, default=1)
    size: int = Field(gt=0, le=50, default=10)
