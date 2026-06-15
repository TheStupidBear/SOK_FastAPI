from model.filament import ProducerFilament
import data.filament as data

def get_all_producer() -> list[ProducerFilament]:
    return data.get_all_producer()
#
# def get_one(name: str) -> Creature | None:
#     return data.get_one(name)
#
# def create(creature: Creature) -> Creature:
#     return data.create(creature)
#
# def modify(name, creature: Creature) -> Creature:
#     return data.modify(name, creature)
#
# def delete(name: str) -> bool:
#     return data.delete(name)