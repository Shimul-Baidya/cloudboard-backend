from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, APIRouter
from apps.schemas.token import Token
from apps.services.auth import authenticate_user, token_exception
from apps.services.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
from sqlalchemy.orm import Session
from apps.database import get_db

router = APIRouter()

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session=Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise token_exception()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, exprires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    




