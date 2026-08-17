from fastapi import APIRouter, Request, UploadFile, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from typing import Annotated
import service.producer_filament as service_producer
import service.color as service_color
import service.type_filament as service_type
import service.example as service_example
import service.user as service_user
from data.producer_filament import init_producer
from data.color import init_color
from data.type_filament import init_type
from data.example import init_example
from pathlib import Path



router = APIRouter(prefix="/filament", tags=["filament"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

# Размер порции данных для чтения (1024 КБ = 1 МБ)
CHUNK_SIZE = 1024 * 1024

#создаем БД с таблицей producer, color, type, example
init_producer()
init_color()
init_type()
init_example()

#получение всех производителей филамента
@router.get("/")
def get_all_producer(request: Request):
    return template_obj.TemplateResponse(
        request=request,
        name="filament.html",
        context={"filaments": service_producer.get_all_producer()})

#получение типов филамента определенного бренда филамента
@router.get("/type/{producer}", name="show_type")
def show_type(request: Request, producer: str):
    return template_obj.TemplateResponse(
        request=request,
        name="type.html",
        context={"producer": producer,
                 "types": service_type.get_producer_type(producer)})

#получение цветов определенного бренда и типа филамента
@router.get("/color/{producer}/{typefil}", name="show_color")
def show_color(request: Request, producer: str, typefil: str):
    type_connection = f"{typefil.lower()}_{producer.lower()}"
    return template_obj.TemplateResponse(
        request=request,
        name="color.html",
        context={"type_connection": type_connection,
                "colors": service_color.get_producer_color(type_connection)})

# получение примеров изделий по цвету
@router.get("/example/{type_connection}/{color}", name="show_example")
def show_example(request: Request, type_connection: str, color: str):
    color_connection = f"{color.lower()}_{type_connection}"
    print(color_connection)
    return template_obj.TemplateResponse(
        request=request,
        name="example.html",
        context={"color": color,
                 "color_connection": color_connection,
                 "examples": service_example.get_color_example(color_connection)})


#добавить пример
@router.get("/add_example/{color_connection}", name="add_example")
def add_example(request: Request, color_connection: str,
                username: Annotated[str, Depends(service_user.get_current_user)],):
    return template_obj.TemplateResponse(
        request=request,
        name="add_example.html",
        context={"color_connection": color_connection,
                 "username": username})


#поиск по цвету
@router.get('/search_color')
def search_items(request: Request, q: str):
    q = q.lower() #понижаем регистр названия цвета
    colors = service_color.get_search_color(q)
    return template_obj.TemplateResponse(
        request=request,
        name="search_color.html",
        context={"colors": colors,
               "q": q})


#загрузка фото и описания
@router.post("/upload_image/{color_connection}/{username}", name="upload_image")
async def create_upload_file(color_connection: str, request: Request,
                             username: str,
                             file: UploadFile, desc: str = Form(...),):
    #если файл не изображение
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Недопустимый тип файла")
    else:
        await service_example.upload_file(parent_dir, file, desc, color_connection, username)
        add_example_message = "Добавили ваш пример"

        return template_obj.TemplateResponse(
            request=request,
            name="example.html",
            context={"color_connection": color_connection,
                     "add_example_message": add_example_message,
                     "examples": service_example.get_color_example(color_connection)})