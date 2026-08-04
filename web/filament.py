from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
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
from typing import Annotated



router = APIRouter(prefix="/filament", tags=["filament"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем БД с таблицей producer, color, type, example
init_producer()
init_color()
init_type()
init_example()


@router.get("/")
def get_all_producer(request: Request):
    return template_obj.TemplateResponse(
        request=request,
        name="filament.html",
        context={"filaments": service_producer.get_all_producer()})

#получение типов филамента определенного бренда филамента
@router.get("/{producer}", name="show_type")
def get_color(request: Request, producer: str):
    return template_obj.TemplateResponse(
        request=request,
        name="type.html",
        context={"producer": producer,
                 "types": service_type.get_producer_type(producer)})

#получение цветов определенного бренда и типа филамента
@router.get("/{producer}/{typefil}", name="show_color")
def get_color(request: Request, producer: str, typefil: str):
    return template_obj.TemplateResponse(
        request=request,
        name="color.html",
        context={"producer": producer,
                 "typefil": typefil,
                 "colors": service_color.get_producer_color(producer, typefil)})


# получение примеров изделий по цвету
@router.get("/{producer}/{typefil}/{color}", name="show_example")
def get_color(request: Request, producer: str, typefil: str, color: str):
    return template_obj.TemplateResponse(
        request=request,
        name="example.html",
        context={"producer": producer,
                 "typefil": typefil,
                 "color": color,
                 "examples": service_example.get_color_example(producer, typefil, color)})
