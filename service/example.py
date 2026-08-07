from model.filament import Example
import data.example as data

def get_color_example(color_connection) -> list[Example]:
    return data.get_color_example(color_connection)

def create_example(example: Example) -> str:
    return data.create(example)
