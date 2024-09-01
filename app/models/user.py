from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    given_name: str
    family_name: str
    password: str

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    given_name: str
    family_name: str
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_staff: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserClaims(BaseModel):
    sub: str
    username: str = None
    email: str = None
    email_verified: bool = False
    given_name: str
    family_name: str
    is_staff: bool = False
    aud: str = None
    iss: str = None
    iat: int
    exp: int
