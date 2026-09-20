from model.filament import Example
import data.example as data
import aiofiles

# Размер порции данных для чтения (1024 КБ = 1 МБ)
CHUNK_SIZE = 1024 * 1024

def get_examples(color_connection) -> list[Example]:
    return data.get_examples(color_connection)

def get_some_example(printer) -> Example:
    return data.get_some_example(printer)

async def create_example(color_connection, username, file, printer, extruder_temperature,
                                       table_temperature, desc) -> str:
    example = Example(printer=printer, extruder_temperature=extruder_temperature,
                      table_temperature=table_temperature, desc=desc,
                      color_connection=color_connection,
                      image=f"/static/image_example/{file.filename}", user=username)
    return data.create(example)

#сохраняем изображение на диск
async def upload_file(parent_dir, file):
    file_path = f"{parent_dir}/static/image_example/{file.filename}"
    # Открываем целевой файл асинхронно для записи байтов ("wb")
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(CHUNK_SIZE):
            await out_file.write(content)


