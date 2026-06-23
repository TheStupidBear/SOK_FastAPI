from pydantic import BaseModel
from typing import Optional


#модель примеров
class Example(BaseModel):
    id: int
    desc: Optional[str] = None  # необязательное поле
    image: str #расположение файла

#модель цвета филамента
class Color(BaseModel):
    name: str
    hex: Optional[str] = None #необязательное поле
    image: str #расположение файла
    # color_type_producer: str
    example: list[Example] = [] #список примеров цвета

#тип филамента
class FilamentType(BaseModel):
    name: str
    # type_producer: str
    color: list[Color] = []


#производитель филамента (содержит название фирмы и список цветов филамента)
class ProducerFilament(BaseModel):
    name: str
    type: list[FilamentType] = []



