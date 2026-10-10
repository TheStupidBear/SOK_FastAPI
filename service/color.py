from model.filament import Color
import data.color as data
import requests
from pathlib import Path

def get_producer_color(type_connection) -> list[Color]:
    return data.get_producer_color(type_connection)

def get_search_color(hex) -> list[Color]:
    return data.get_search_color(hex)


def hex_to_image(parent_dir, hex, name, type_connection):
    file_path = file_path_color(parent_dir, name, type_connection)
    url = f"https://singlecolorimage.com/get/{hex}/150x150"
    response = requests.get(url=url)
    #Проверка статуса и вывод HTML-кода ответа
    if response.status_code == 200:
        # сохраняем на диск
        out = open(file_path, "wb")
        out.write(response.content)
        out.close()
    else:
        print(f"Ошибка: {response.status_code}")

def create_color(hex, name, type_connection):
    split_type_conn = type_connection.split("_")  # список из типа и производителя
    file_path = f"/static/image_color/{split_type_conn[1]}/{split_type_conn[0]}/{name}.jpg"
    color_type_producer = f"{hex}_{type_connection}"
    color = Color(color_type_producer=color_type_producer, name=name, hex=hex,
                  image=file_path,
                  type_connection=type_connection)
    data.create(color)

def file_path_color(parent_dir, name, type_connection):
    split_type_conn = type_connection.split("_")  # список из типа и производителя
    file_path = Path(f"{parent_dir}/static/image_color/{split_type_conn[1]}/{split_type_conn[0]}/{name}.jpg")
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Создаем все родительские папки
    return file_path