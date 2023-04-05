from dataclasses import dataclass
from typing import Dict

from collection.items.item import Item


@dataclass
class Alignment(Item):
    id: str
    title: str
    bdrc_work_id: str = None
    path: str
