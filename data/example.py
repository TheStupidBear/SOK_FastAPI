import sqlite3
from model.filament import Example
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')

# создание БД для цвета (связана с типом филамента)
def init_example():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists example(
     id integer primary key,
     desc text, 
     image text,
     color_connection text,
     FOREIGN KEY (color_connection) REFERENCES color(color_type_producer))""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Example:
    id = row[0]
    desc = row[1]
    image = row[2]
    return Example(id=id, desc=desc, image=image)

#преобразует обьект модели в словарь
def model_to_dict(example: Example) -> dict:
    return example.dict()


def get_color_example(producer, typefil, color) -> list[Example]:
    color_connection = f"{color.lower()}_{typefil.lower()}_{producer.lower()}"
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from example where color_connection=:color_connection"
    params = {"color_connection": color_connection}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    print(rows)
    conn.close()
    return [row_to_model(row) for row in rows]
