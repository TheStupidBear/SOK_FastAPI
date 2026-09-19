from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Annotated
import service.user as service_user
from data.color import init_color
import service.color as service_color

router = APIRouter(prefix="/color", tags=["color"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")
#создаем БД color
init_color()

#получение цветов определенного бренда и типа филамента
@router.get("/colors/{producer}/{typefil}", name="show_color")
def show_color(request: Request, producer: str, typefil: str):
    type_connection = f"{typefil.lower()}_{producer.lower()}"
    return template_obj.TemplateResponse(
        request=request,
        name="color.html",
        context={"type_connection": type_connection,
                "colors": service_color.get_producer_color(type_connection)})

#добавить цвет
@router.get("/add_color/{type_connection}", name="add_color")
def add_example(request: Request, type_connection: str,
                username: Annotated[str, Depends(service_user.get_current_user)],):
    return template_obj.TemplateResponse(
        request=request,
        name="add_color.html",
        context={"type_connection": type_connection})

#поиск по цвету
@router.get('/search_color')
def search_items(request: Request, q: str):
    q = q.lower() #понижаем регистр hex
    colors = service_color.get_search_color(q)
    return template_obj.TemplateResponse(
        request=request,
        name="search_color.html",
        context={"colors": colors,
               "q": q})

#создание цвета
@router.post("/create_color/{type_connection}", name="create_color")
async def create_upload_file(type_connection: str, request: Request,
                             name: str = Form(...), hex: str = Form(...)):
    hex = hex.lower() #понижаем регистр
    service_color.hex_to_image(parent_dir, hex, name)
    service_color.create_color(hex, name, type_connection)
    return template_obj.TemplateResponse(
        request=request,
        name="color.html",
        context={"type_connection": type_connection,
                 "colors": service_color.get_producer_color(type_connection)})