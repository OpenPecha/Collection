from pathlib import Path
from typing import List

from openpecha.serializers.hfml import HFMLSerializer
from collection.items.pecha import Pecha, PechaFragment

from collection.items.item import Item
from collection.views.view import View, ViewSerializer


class HFMLViewSerializer(ViewSerializer):
    def serialize(self, item: Item, output_dir: Path)->List[Path]:
        serializer = HFMLSerializer(f"{item.path}/{item.path.stem}.opf")
        serializer.apply_layers()
        serialized_results = serializer.get_result()
        if isinstance(item,Pecha):
            view_paths = self.serialize_pecha(serialized_results, output_dir)
        elif isinstance(item,PechaFragment):
            view_paths = self.serialize_pecha_fragment(serialized_results,output_dir,item)
        return view_paths

    def serialize_pecha(self, serialized_results, output_dir: Path) -> List[Path]:
        view_paths = []
        for base_name, hfml_text in serialized_results.items():
            view_path = (output_dir / f"{base_name}.txt")
            view_path.write_text(hfml_text, encoding="utf-8")
            view_paths.append(view_path)
        
        return view_paths
    
    def serialize_pecha_fragment(self, serialized_results, output_dir: Path,pecha_fragment:PechaFragment):
        view_paths = []
        spans = pecha_fragment.spans

        for base_name, hfml_text in serialized_results.items():

            view_path = (output_dir / f"{base_name}.txt")


        

class HFMLView(View):
    def __init__(self) -> None:
        self.__name__ = "hfml"
        self.serializer = HFMLViewSerializer
        super().__init__(self.__name__ , self.serializer)

    def save_catalog(self, collection_dir: Path, itmes: List[Item]):
        catalog_file_path = collection_dir / f"Catalog_{self.name}.csv"
        field_names = ["FILE NAME", "TITLE", "OP ID", "BDRC ID", "VOLUME NUMBER"]
        pass
