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
    name = row[1]
    hex = row[2]
    image = row[3]
    type_connection = row[4]
    return Color(name=name, hex=hex, image=image, type_connection=type_connection)

#преобразует обьект модели в словарь
def model_to_dict(color: Color) -> dict:
    return color.dict()


def get_producer_color(producer, typefil) -> list[Color]:
    type_connection = f"{typefil.lower()}_{producer.lower()}"
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from color where type_connection=:type_connection"
    params = {"type_connection": type_connection}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    print(rows)
    conn.close()
    return [row_to_model(row) for row in rows]


def get_search_color(name) -> list[Color]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from color where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    print(rows)
    conn.close()
    return [row_to_model(row) for row in rows]