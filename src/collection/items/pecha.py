from dataclasses import dataclass
from typing import Dict

from collection.items.item import Item


@dataclass
class Pecha(Item):
    id: str
    title: str
    bdrc_work_id: str
    path: str


if __name__ == "__main__":
    print(Pecha.__annotations__)


class PechaFragment(Pecha):
    "span= {'base':(start,end)}"
    span: Dict
