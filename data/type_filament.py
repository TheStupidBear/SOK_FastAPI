import sqlite3
from model.filament import FilamentType
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')

# создание БД для цвета (связана с фирмой филамента
def init_type():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists type(
     type_producer text primary key,
     name text,
     producer_name text,  
     FOREIGN KEY (producer_name) REFERENCES producer(name))""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> FilamentType:
    name = row[1]
    type_producer = row[0]
    return FilamentType(name=name, type_producer=type_producer)

#преобразует обьект модели в словарь
def model_to_dict(type: FilamentType) -> dict:
    return type.dict()


def get_producer_type(producer) -> list[FilamentType]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from type where producer_name=:producer"
    params = {"producer": producer}
    curs.execute(qry, params)
    rows = list(curs.fetchall())
    print(f"rows - {rows}")
    conn.close()
    return [row_to_model(row) for row in rows]