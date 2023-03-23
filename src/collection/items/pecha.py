from collection.items.item import Item
from dataclasses import dataclass

@dataclass(frozen=True)
class PechaMeta:
    id: str
    title: str
    bdrc_id: str
    volume_number:str
    base_name:str
    pecha_path:str

class Pecha(Item):

    def __init__(self, id, title, bdrc_id, volume_number, base_name, pecha_path) -> None:
        self.id = id
        self.title = title
        self.bdrc_id = bdrc_id
        self.volume_number = volume_number
        self.base_name = base_name
        self.pecha_path = pecha_path

if __name__ == "__main__":
    print(PechaMeta.__annotations__)