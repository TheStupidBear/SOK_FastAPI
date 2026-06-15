from pydantic import BaseModel
from typing import Optional

#модель изображения
class Image(BaseModel):
    url: str
    name: str

#модель примеров
class Example(BaseModel):
    name: str
    desc: Optional[str] = None  # необязательное поле
    image: Image

#модель цвета филамента
class Color(BaseModel):
    name: str
    hex: Optional[str] = None #необязательное поле
    image: Image

#производитель филамента (содержит название фирмы и список цветов филамента)
class ProducerFilament(BaseModel):
    name: str
    # color: list[Color]|None = None



