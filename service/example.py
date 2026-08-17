from model.filament import Example
import data.example as data
import aiofiles

# Размер порции данных для чтения (1024 КБ = 1 МБ)
CHUNK_SIZE = 1024 * 1024

def get_color_example(color_connection) -> list[Example]:
    return data.get_color_example(color_connection)

def create_example(example: Example) -> str:
    return data.create(example)

async def upload_file(parent_dir, file, desc, color_connection, username):
    file_path = f"{parent_dir}/static/image_example/{file.filename}"
    # Открываем целевой файл асинхронно для записи байтов ("wb")
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(CHUNK_SIZE):
            await out_file.write(content)
    example = Example(desc=desc, color_connection=color_connection,
                      image=f"/static/image_example/{file.filename}", user=username)
    create_example(example)

