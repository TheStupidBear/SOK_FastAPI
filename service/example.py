from model.filament import Example
import data.example as data
import aiofiles
from pathlib import Path

# Размер порции данных для чтения (1024 КБ = 1 МБ)
CHUNK_SIZE = 1024 * 1024

def get_examples(color_connection) -> list[Example]:
    return data.get_examples(color_connection)

def get_some_example(id) -> Example:
    return data.get_some_example(id)

def up_rating_example(id) -> Example:
    return data.up_rating_example(id)

def down_rating_example(id) -> Example:
    return data.down_rating_example(id)

async def create_example(color_connection, username, file, printer, extruder_temperature,
                                       table_temperature, desc) -> str:
    split_color_conn = color_connection.split("_")  # список из цвета, типа и производителя
    producer = split_color_conn[-1]
    type_fil = split_color_conn[-2]
    list_color = split_color_conn[:-2]  # список без производителя и типа
    color = '_'.join(list_color)  # получаем название цвета
    example = Example(printer=printer, extruder_temperature=extruder_temperature,
                      table_temperature=table_temperature, desc=desc,
                      color_connection=color_connection,
                      image=f"/static/image_example/{producer}/{type_fil}/{color}/{file.filename}.jpg",
                      user=username)
    return data.create(example)

#сохраняем изображение на диск
async def upload_file(parent_dir, file, color_connection):
    split_color_conn = color_connection.split("_")  # список из цвета, типа и производителя
    producer = split_color_conn[-1]
    type_fil = split_color_conn[-2]
    list_color = split_color_conn[:-2] #список без производителя и типа
    color = '_'.join(list_color) #получаем название цвета
    file_path = Path(f"{parent_dir}/static/image_example/{producer}/{type_fil}/{color}/{file.filename}.jpg")
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Создаем все родительские папки
    # Открываем целевой файл асинхронно для записи байтов ("wb")
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(CHUNK_SIZE):
            await out_file.write(content)


