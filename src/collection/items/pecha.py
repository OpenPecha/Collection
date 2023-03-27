from collection.items.item import Item
from dataclasses import dataclass

@dataclass(frozen=True)
class Pecha:
    id: str
    title: str
    bdrc_id: str
    volume_number:str
    base_name:str
    pecha_path:str

if __name__ == "__main__":
    print(Pecha.__annotations__)