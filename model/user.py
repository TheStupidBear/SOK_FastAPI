from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    is_admin: int = 0 # 1 - админ, 0 - обычный пользователь