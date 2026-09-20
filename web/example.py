from fastapi import APIRouter, Request, Depends, Form, UploadFile, HTTPException
from pathlib import Path
from fastapi.templating import Jinja2Templates
from typing import Annotated
from data.example import init_example
import service.example as service_example
import service.user as service_user


router = APIRouter(prefix="/example", tags=["example"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем БД example
init_example()


# получение примеров изделий по цвету
@router.get("/examples/{type_connection}/{color}", name="show_examples")
def show_examples(request: Request, type_connection: str, color: str):
    color_connection = f"{color.lower()}_{type_connection}"
    print(color_connection)
    return template_obj.TemplateResponse(
        request=request,
        name="examples.html",
        context={"color": color,
                 "color_connection": color_connection,
                 "examples": service_example.get_examples(color_connection)})

#получение отдельного примера (example)
@router.get("/some_example/{printer}", name="show_some_example")
def show_some_example(request: Request, printer: str):
    example = service_example.get_some_example(printer)
    return template_obj.TemplateResponse(
        request=request,
        name="some_example.html",
        context={"example": example})


#добавить пример
@router.get("/add_example/{color_connection}", name="add_example")
def add_example(request: Request, color_connection: str,
                username: Annotated[str, Depends(service_user.get_current_user)],):
    return template_obj.TemplateResponse(
        request=request,
        name="add_example.html",
        context={"color_connection": color_connection,
                 "username": username})



#добавление примера
@router.post("/upload_exampe/{color_connection}/{username}", name="upload_example")
async def create_upload_file(color_connection: str, request: Request,
                             username: str, file: UploadFile,
                             printer: str = Form(...),
                             extruder_temperature: str | None = Form(default=None),
                             table_temperature: str | None = Form(default=None),
                             desc: str | None = Form(default=None),):
    #если файл не изображение
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Недопустимый тип файла")
    else:
        await service_example.upload_file(parent_dir, file)
        await service_example.create_example(color_connection, username,
                                             file, printer, extruder_temperature,
                                       table_temperature, desc)
        add_example_message = "Добавили ваш пример"

        return template_obj.TemplateResponse(
            request=request,
            name="examples.html",
            context={"color_connection": color_connection,
                     "add_example_message": add_example_message,
                     "examples": service_example.get_examples(color_connection)})