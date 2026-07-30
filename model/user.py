from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    is_superuser: int = 0 # 1 - админ, 0 - обычный пользователь

class Token(BaseModel):
    access_token: str
    token_type: str
