from pydantic import BaseModel



#модель примеров
class Example(BaseModel):
    desc: str
    image: str #расположение файла
    color_connection: str #связь с поределенным цветом
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



