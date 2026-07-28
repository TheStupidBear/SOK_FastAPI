from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from model.user import User

router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret",
        "is_admin": 0,
    },
    "alice": {
        "username": "alice",
        "password": "fakehashedsecret2",
        "is_admin": 1,
    },
}



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = User(**user_dict)
    if not form_data.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user