from model.filament import ProducerFilament
import data.filament as data

def get_all_producer() -> list[ProducerFilament]:
    return data.get_all_producer()
