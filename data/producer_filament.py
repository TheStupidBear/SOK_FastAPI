import sqlite3
from model.filament import ProducerFilament
import os

# 1. Получаем путь к родительской папке (выше текущей)
parent_dir = os.path.dirname(os.getcwd())

# 2. Формируем полный путь к базе данных
db_path = os.path.join(parent_dir, 'filament.db')

#создание БД
def init_producer():
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("""create table if not exists producer(
     name text primary key)""")
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

#преобразует кортеж в обьект модели
def row_to_model(row: tuple) -> ProducerFilament:
    name = row[0]
    return ProducerFilament(name=name)

#преобразует обьект модели в словарь
def model_to_dict(creature: ProducerFilament) -> dict:
    return creature.dict()



def get_all_producer() -> list[ProducerFilament]:
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    qry = "select * from producer"
    curs.execute(qry)
    rows = list(curs.fetchall())
    conn.close()
    return [row_to_model(row) for row in rows]


