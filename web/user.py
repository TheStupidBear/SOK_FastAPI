from fastapi import APIRouter, Depends, Request, Form
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
import secrets
from model.user import Token, User
import service.user as service
from data.user import init_user

router = APIRouter(prefix="/user", tags=["user"])

#создаем БД
init_user()

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#страница с формой логина
@router.get("/login")
async def login(request: Request):
    return template_obj.TemplateResponse(
        request=request,
        name="login.html")

#проверка логина и возврат токена
@router.post("/get_token")
async def get_token(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    #получаем токен и возращаем клиенту
    token = await service.login_for_access_token(username, password)
    print(f"token - {token}")
    return template_obj.TemplateResponse(
        request=request,
        name="success_login.html",
        context={"request": request,
                "token": token.access_token})


#страница регистрации
@router.get("/registration")
async def registration(request: Request):
    return template_obj.TemplateResponse(request=request,
                                         name="registration.html")


@router.post("/send_registration")
async def reg(request: Request, username: str = Form(...), password: str = Form(...),
              repeat_password: str = Form(...)):
    #проверка паролей (они одинаковы или нет)
    current_password_bytes = password.encode("utf8")
    correct_password_bytes = repeat_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_password:  # если пароли не совпадают
        message = "Пароли не совпадают"
        return template_obj.TemplateResponse(request=request,
                                             name="registration.html",
                                             context={"message": message})
    else:
        if service.check_user(username):  # если есть в БД такой пользователь
            message = "Такой пользователь уже есть"
            return template_obj.TemplateResponse(request=request,
                                                 name="registration.html",
                                                 context={"message": message})
        else:
            service.create(User(username=username, password=password))
            # получаем токен и возращаем клиенту
            token = await service.login_for_access_token(username, password)
            return template_obj.TemplateResponse(request=request,
                                                 name="index.html",
                                                 context={"token": token.access_token})

@router.get("/me")
async def read_users_me(
    username: Annotated[str, Depends(service.get_current_user)],
) -> str:
    return username


# для swagger (docs)
@router.post("/token")
async def token(username: Annotated[str, Form()], password: Annotated[str, Form()]) -> Token:
    token = await service.login_for_access_token(username, password)
    return token