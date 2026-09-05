from model.filament import Color
import data.color as data
import requests

def get_producer_color(type_connection) -> list[Color]:
    return data.get_producer_color(type_connection)

def get_search_color(hex) -> list[Color]:
    return data.get_search_color(hex)


def hex_to_image(parent_dir, hex, name):
    file_path = f"{parent_dir}/static/image_color/{name}.jpg"
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
    color_type_producer = f"{hex}_{type_connection}"
    color = Color(color_type_producer=color_type_producer, name=name, hex=hex,
                  image=f"/static/image_color/{name}.jpg",
                  type_connection=type_connection)
    data.create(color)
