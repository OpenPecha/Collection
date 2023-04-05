from pathlib import Path
from typing import List

from openpecha.serializers.hfml import HFMLSerializer

from collection.items.item import Item
from collection.views.view import View, ViewSerializer


class HFMLViewSerializer(ViewSerializer):
    def serialize(self, pecha, output_dir):
        serializer = HFMLSerializer(opf_path=pecha.pecha_path)
        serializer.apply_layers()
        serialized_results = serializer.get_result()
        for base_name, hfml_text in serialized_results.items():
            (output_dir / f"{base_name}.txt").write_text(hfml_text, encoding="utf-8")


class HFMLView(View):
    def __init__(self, name: str, serializer_class: HFMLViewSerializer) -> None:
        self.__name__ = name
        super().__init__(name, serializer_class)

    def save_catalog(self, collection_dir: Path, itmes: List[Item]):
        catalog_file_path = collection_dir / f"Catalog_{self.name}.csv"
        field_names = ["FILE NAME", "TITLE", "OP ID", "BDRC ID", "VOLUME NUMBER"]
        pass
