from dataclasses import dataclass
from collection.items.pecha import Pecha,PechaFragment
from collection.items.alignment import Alignment
from collection.items.work import Work
from enum import Enum


@dataclass
class Item:
    id: str

class ItemEnum(Enum):
    pecha =  Pecha
    alignment = Alignment
    work = Work
    pecha_fragment = PechaFragment