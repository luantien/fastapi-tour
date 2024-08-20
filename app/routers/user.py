from typing import List
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import User
from models import UserViewModel, UserBaseModel

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserBaseModel])
async def get_users(db: Session = Depends(get_db_context)) -> List[UserViewModel]:
    return db.query(User).filter(User.is_active == True).all()
