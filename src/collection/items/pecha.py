from dataclasses import dataclass
from typing import Dict

from collection.items.item import Item


@dataclass
class Pecha(Item):
    id: str
    title: str
    bdrc_work_id: str
    path: str


@dataclass
class PechaFragment(Item):
    "span= {'base':(start,end)}"
    id: str
    title: str
    bdrc_work_id: str
    path: str
    spans: Dict[str, Dict]
