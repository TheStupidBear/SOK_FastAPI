from pydantic import BaseModel
from typing import Optional



#модель примеров
class Example(BaseModel):
    id: Optional[int] = None
    printer: str
    table_temperature: Optional[int] = None #необязательное значение
    extruder_temperature: Optional[int] = None
    desc: Optional[str] = None
    image: str #расположение файла
    color_connection: str #связь с определенным цветом
    user: str #пользователь

#модель цвета филамента
class Color(BaseModel):
    color_type_producer: str
    name: str
    hex: str
    image: str #расположение файла
    type_connection: str #строка тип-производитель

#тип филамента
class FilamentType(BaseModel):
    name: str


#производитель филамента (содержит название фирмы и список цветов филамента)
class ProducerFilament(BaseModel):
    name: str



