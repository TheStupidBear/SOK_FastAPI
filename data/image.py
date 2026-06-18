import sqlite3
from model.filament import Image
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')


# создание БД для цвета
# def init_image():
#     conn = sqlite3.connect(db_path)
#     curs = conn.cursor()
#     curs.execute("""create table if not exists image(
#      id text primary key,
#      url text,
#      FOREIGN KEY (color_name) REFERENCES color(name))""")
#     # Сохраняем изменения и закрываем соединение
#     conn.commit()
#     conn.close()

#преобразует кортеж в обьект модели
# def row_to_model(row: tuple) -> Color:
#     name, hex = row
#     return Color(name=name, hex=hex)
#
# #преобразует обьект модели в словарь
# def model_to_dict(color: Color) -> dict:
#     return color.dict()
#
#
#
# def get_all_color() -> list[Color]:
#     conn = sqlite3.connect(db_path)
#     curs = conn.cursor()
#     qry = "select * from color"
#     curs.execute(qry)
#     rows = list(curs.fetchall())
#     conn.close()
#     return [row_to_model(row) for row in rows]