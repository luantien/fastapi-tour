
from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db_context
from services import user as UserService
from services.exception import UnAuthorizedError
from settings import COGNITO

router = None

if not COGNITO["ENABLED"]:
    router = APIRouter(prefix="/auth", tags=["Auth"])
    @router.post("/token")
    async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_context)
        ):
            user = UserService.authenticate_user(form_data.username, form_data.password, db)

            if not user:
                raise UnAuthorizedError()

            return {
                "token_type": "bearer",
                "access_token":  UserService.create_access_token(
                    user, 
                    int(timedelta(minutes=10).total_seconds())
                ),
            }
