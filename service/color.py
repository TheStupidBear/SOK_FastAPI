from model.filament import Color
import data.color as data

def get_producer_color(producer) -> list[Color]:
    return data.get_producer_color(producer)
