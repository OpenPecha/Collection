from pathlib import Path
from typing import List, Type
from enum import Enum

from collection.items.item import Item


class ViewSerializer:
    __name__ = "ViewSerializer"

    def __init__(self) -> None:
        pass

    def serialize(self, item, output_dir: Path):
        return NotImplementedError("Please implement your serializer")


class View:
    __name__ = "View"

    def __init__(self, name: str, serializer_class: Type[ViewSerializer]) -> None:
        self.name = name
        self.serializer_class = serializer_class

    def to_dict(self) -> dict:
        return {"name": self.name, "serializer_class": self.serializer_class.__name__}

    def save_catalog(self, collection_dir: Path, items: List[Item]):
        return NotImplementedError("Please implement save catalog")

class ViewEnum(Enum):
    plain