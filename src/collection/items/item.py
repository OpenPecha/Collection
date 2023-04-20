from dataclasses import dataclass


@dataclass
class Item:
    id: str

    def serialize(self, serializer, output_dir):
        return NotImplementedError("Please implement your serializer")
