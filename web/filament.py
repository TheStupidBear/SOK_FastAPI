from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import service.filament as service_producer
import service.color as service_color
from data.filament import init_producer
from data.color import init_color
from pathlib import Path



router = APIRouter(prefix="/filament", tags=["filament"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем БД с таблицей producer, color
init_producer()
init_color()

@router.get("")
@router.get("/")
def get_all_producer(request: Request):
    return template_obj.TemplateResponse(
        request=request,
        name="filament.html",
        context={"filaments": service_producer.get_all_producer()})

#получение цветов определенного бренда филамента
@router.get("{producer}", name="show_color")
@router.get("/{producer}", name="show_color")
def get_color(request: Request, producer: str):
    print(producer)
    return template_obj.TemplateResponse(
        request=request,
        name="color.html",
        context={"producer": producer,
                 "colors": service_color.get_producer_color(producer)})
