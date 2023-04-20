from pathlib import Path
from typing import List

from openpecha.serializers.hfml import HFMLSerializer
from collection.items.pecha import Pecha, PechaFragment
from collection.items.work import Work

from collection.items.item import Item
from collection.views.view import View, ViewSerializer


class HFMLViewSerializer(ViewSerializer):
    """
    Class represting the HFML View Serializer
    """
    def serialize(self, item: Item, output_dir: Path)->List[Path]:
        """
        This function calls the particular serializer based on item

        :param item: Item to be serialize
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        
        if isinstance(item,Pecha):
            view_paths = self.serialize_pecha(item, output_dir)
        elif isinstance(item,Work):
            view_paths = self.serialize_work(item,output_dir)
        else:
            raise ValueError(f"{item} Serializer not supported or PlainTextView")
        return view_paths


    def serialize_pecha(self, item, output_dir: Path) -> List[Path]:
        """
        This function serializes the Pecha to hfml

        :param pecha: Pecha object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        serializer = HFMLSerializer(f"{item.path}/{item.path.stem}.opf")
        serializer.apply_layers()
        serialized_results = serializer.get_result()
        view_paths = []
        for base_name, hfml_text in serialized_results.items():
            view_path = (output_dir / f"{base_name}.txt")
            view_path.write_text(hfml_text, encoding="utf-8")
            view_paths.append(view_path)
        return view_paths
    
    
    def serialize_work(self,work:Work,output_dir:Path):
        views_paths = []
        instances = work.instances
        if not instances:
            return
        for instance in instances:
            if isinstance(instance, Pecha):
                views_path = self.serialize_pecha(instance, output_dir)
            elif isinstance(instance, PechaFragment):
                views_path = self.serialize_pecha_fragment(instance, output_dir)
            else:
                raise ValueError(f"{instance} Not a Valid Work Instance")
            views_paths.extend(views_path)
        return views_paths

    
    def serialize_pecha_fragment(self, item, output_dir: Path):
        view_paths = []
        serializer = HFMLSerializer(f"{item.path}/{item.path.stem}.opf")
        serializer.apply_layers()
        serialized_results = serializer.get_result()
        for base_name, hfml_text in serialized_results.items():
            view_path = (output_dir / f"{base_name}.txt")
            view_path.write_text(hfml_text, encoding="utf-8")
            view_paths.append(view_path)
        return view_paths


class HFMLView(View):
    """
    Class representing HFML view

    Attributes
    name: Name of the View
    serializer: Serializer Class
    """
    def __init__(self) -> None:
        self.__name__ = "hfml"
        self.serializer = HFMLViewSerializer
        super().__init__(self.__name__ , self.serializer)

    def save_catalog(self, collection_dir: Path, itmes: List[Item]):
        catalog_file_path = collection_dir / f"Catalog_{self.name}.csv"
        field_names = ["FILE NAME", "TITLE", "OP ID", "BDRC ID", "VOLUME NUMBER"]
        pass
