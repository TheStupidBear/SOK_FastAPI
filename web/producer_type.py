from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import service.producer_filament as service_producer
import service.type_filament as service_type
from data.producer_filament import init_producer
from data.type_filament import init_type
from pathlib import Path



router = APIRouter(prefix="/filament", tags=["filament"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")


#создаем БД с таблицей producer, type
init_producer()
init_type()

#получение всех производителей филамента
@router.get("/")
def get_all_producer(request: Request):
    return template_obj.TemplateResponse(
        request=request,
        name="filament.html",
        context={"filaments": service_producer.get_all_producer()})

#получение типов филамента определенного бренда филамента
@router.get("/{producer}", name="show_type")
def show_type(request: Request, producer: str):
    return template_obj.TemplateResponse(
        request=request,
        name="type.html",
        context={"producer": producer,
                 "types": service_type.get_producer_type(producer)})







