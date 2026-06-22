from pydantic import BaseModel
from typing import Optional

#модель изображения
class Image(BaseModel):
    id: str
    url: str

#модель примеров
class Example(BaseModel):
    name: str
    desc: Optional[str] = None  # необязательное поле
    image: Image

#модель цвета филамента
class Color(BaseModel):
    name: str
    hex: Optional[str] = None #необязательное поле
    image: str #расположение файла

#тип филамента
class FilamentType(BaseModel):
    name: str
    type_producer: str
    color: list[Color] = []


#производитель филамента (содержит название фирмы и список цветов филамента)
class ProducerFilament(BaseModel):
    name: str
    type: list[FilamentType] = []



