import sqlite3
from model.filament import Color
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')

# создание БД для цвета (связана с фирмой филамента
def init_color():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists color(
     name text primary key,
     hex text,
     producer_name text,
     FOREIGN KEY (producer_name) REFERENCES producer(name))""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Color:
    name, hex, producer_name = row
    return Color(name=name, hex=hex, producer_name=producer_name)

#преобразует обьект модели в словарь
def model_to_dict(color: Color) -> dict:
    return color.dict()


def get_producer_color(producer) -> list[Color]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from color where producer_name=:producer"
    params = {"producer": producer}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]
