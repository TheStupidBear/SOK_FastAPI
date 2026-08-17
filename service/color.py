from model.filament import Color
import data.color as data

def get_producer_color(type_connection) -> list[Color]:
    return data.get_producer_color(type_connection)

def get_search_color(name) -> list[Color]:
    return data.get_search_color(name)
