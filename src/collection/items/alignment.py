from dataclasses import dataclass
from pathlib import Path

from collection.items.item import Item


@dataclass
class Alignment(Item):
    id: str
    title: str
    path: Path
    bdrc_work_id: str = None
