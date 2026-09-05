import sqlite3
from model.filament import Color
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')

# создание БД для цвета (связана с типом филамента)
def init_color():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists color(
     color_type_producer text primary key,
     name text,
     hex text,
     image text,
     type_connection text,
     FOREIGN KEY (type_connection) REFERENCES type(type_producer))""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Color:
    color_type_producer = row[0]
    name = row[1]
    hex = row[2]
    image = row[3]
    type_connection = row[4]
    return Color(color_type_producer=color_type_producer, name=name, hex=hex, image=image,
                 type_connection=type_connection)

#преобразует обьект модели в словарь
def model_to_dict(color: Color) -> dict:
    return color.dict()


def get_producer_color(type_connection) -> list[Color]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from color where type_connection=:type_connection"
    params = {"type_connection": type_connection}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]


def get_search_color(hex) -> list[Color]:
    # 4. Формируем шаблон с процентами прямо в значении параметра
    search_pattern = f'%{hex}%'
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from color where hex like ?"
    params = (search_pattern,)
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]


def create(color: Color):
    if not color: return None
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = """insert into color (color_type_producer, name, hex, image, type_connection) values
        (:color_type_producer, :name, :hex, :image, :type_connection)"""
    params = model_to_dict(color)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise f"Color {color.name} already exists"
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return color.name