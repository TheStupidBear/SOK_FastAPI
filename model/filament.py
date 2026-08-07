from pydantic import BaseModel
from typing import Optional
from model.user import User


#модель примеров
class Example(BaseModel):
    desc: str
    image: str #расположение файла
    color_connection: str #связь с поределенным цветом
    user: str #пользователь

#модель цвета филамента
class Color(BaseModel):
    name: str
    hex: Optional[str] = None #необязательное поле
    image: str #расположение файла
    example: list[Example] = [] #список примеров цвета

#тип филамента
class FilamentType(BaseModel):
    name: str
    color: list[Color] = []


#производитель филамента (содержит название фирмы и список цветов филамента)
class ProducerFilament(BaseModel):
    name: str
    type: list[FilamentType] = []



