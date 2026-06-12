from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import service.filament as service
from data.filament import init_producer
from pathlib import Path



router = APIRouter(prefix="/filament", tags=["filament"])

parent_dir = Path(__file__).resolve().parent.parent
template_obj = Jinja2Templates(directory=f"{parent_dir}/template")

#создаем БД с таблицей producer
init_producer()

@router.get("")
@router.get("/")
def get_all(request: Request):
    return service.get_all()