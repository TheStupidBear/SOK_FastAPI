from model.filament import Example
import data.example as data

def get_color_example(producer, typefil, color) -> list[Example]:
    return data.get_color_example(producer, typefil, color)