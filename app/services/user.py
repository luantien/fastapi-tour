from typing import Optional
from datetime import timedelta

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import UserClaims
from entities.user import User, verify_password
from services.utils import get_current_timestamp
from settings import JWT_ALGORITHM, JWT_SECRET


def create_access_token(user: User, expires: Optional[int] = None):
    claims = UserClaims(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        email_verified=True,
        given_name=user.given_name,
        family_name=user.family_name,
        is_staff=user.is_staff,
        aud='FastAPI',
        iss='FastAPI',
        iat=get_current_timestamp(),
        exp=get_current_timestamp() + expires if expires else get_current_timestamp() + int(timedelta(minutes=10).total_seconds())
    )
    return jwt.encode(claims.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)

def authenticate_user(username: str, password: str, db: Session):
    user = db.scalars(select(User).filter(User.username == username)).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user