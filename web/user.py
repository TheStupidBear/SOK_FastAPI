from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from model.user import User, Token
import service.user as service
from data.user import init_user, login_user

router = APIRouter(prefix="/user", tags=["user"])

#создаем БД
init_user()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # если есть такой пользователь в БД
    if login_user(form_data.username, form_data.password):
        access_token_expires = timedelta(minutes=service.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = service.create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )



@router.get("/me")
async def read_users_me(
    username: Annotated[str, Depends(service.get_current_user)],
) -> str:
    return username


@router.get("/me/items")
async def read_own_items(
    username: Annotated[str, Depends(service.get_current_user)],
):
    return [{"item_id": "Foo", "owner": username}]