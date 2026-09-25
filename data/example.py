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
     printer text, 
     table_temperature integer,
     extruder_temperature integer,
     desc text, 
     image text,
     user text,
     color_connection text,
     FOREIGN KEY (color_connection) REFERENCES color(color_type_producer))""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> Example:
    id = row[0]
    printer = row[1]
    table_temperature = row[2]
    extruder_temperature = row[3]
    desc = row[4]
    image = row[5]
    user = row[6]
    color_connection = row[7]
    return Example(id=id, printer=printer, table_temperature=table_temperature,
                   extruder_temperature=extruder_temperature, desc=desc,
                   image=image, user=user, color_connection=color_connection)

#преобразует обьект модели в словарь
def model_to_dict(example: Example) -> dict:
    return example.dict()


def get_examples(color_connection) -> list[Example]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from example where color_connection=:color_connection"
    params = {"color_connection": color_connection}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]

def get_some_example(id) -> Example:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from example where id=:id"
    params = {"id": id}
    curs.execute(qry, params)
    row = curs.fetchone() #получаем один пример
    conn.close()
    if row:  # если не пустой
        return row_to_model(row)
    else:
        print(f"Пример не найден")

def create(example: Example):
    if not example: return None
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = """insert into example (printer, table_temperature, extruder_temperature,
             desc, image, color_connection, user) values
            (:printer, :table_temperature, :extruder_temperature,
             :desc, :image, :color_connection, :user)"""
    params = model_to_dict(example)
    try:
        curs.execute(qry, params)
    except sqlite3.IntegrityError:
        raise f"Example {example.desc} already exists"
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    return example.desc