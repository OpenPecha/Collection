from collection.items.item import Item
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Pecha:
    id: str
    title: str
    bdrc_work_id: str
    path:str

if __name__ == "__main__":
    print(Pecha.__annotations__)

class PechaFragment(Pecha):
    "span= {'base':(start,end)}"
    span: Dict