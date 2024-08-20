
from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db_context
from services import auth as AuthService
from services.exception import UnAuthorizedError


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_context)
    ):
        user = AuthService.authenticate_user(form_data.username, form_data.password, db)

        if not user:
            raise UnAuthorizedError()

        return {"access_token":  AuthService.create_access_token(user, timedelta(minutes=10)), "token_type": "bearer"}
