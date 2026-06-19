from model.filament import FilamentType
import data.type_filament as data

def get_producer_type(producer) -> list[FilamentType]:
    return data.get_producer_type(producer)