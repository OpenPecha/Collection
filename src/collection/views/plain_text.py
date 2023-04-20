from pathlib import Path
from typing import List

from collection.items.item import Item
from collection.items.pecha import Pecha, PechaFragment
from collection.items.work import Work
from collection.views.view import View, ViewSerializer
from collection.utils import get_opf_bases,get_fragment_id

class PlainTextViewSerializer(ViewSerializer):
    """
    Class represeting the PlainText View Serializer
    """

    def serialize_pecha(self, pecha: Pecha, output_dir: Path):
        """
        This function serializes the Pecha to plaintext

        :param pecha: Pecha object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        views_path = []
        bases = get_opf_bases(pecha.path)
        for base in bases:
            base_text = base.read_text(encoding="utf-8")
            view_path = output_dir / f"{base.name}"
            view_path.write_text(base_text, encoding="utf-8")
            views_path.append(view_path)
        return views_path


    def serialize_pecha_fragment(self, pecha_fragment: PechaFragment, output_dir: Path):
        """
        This function serializes the PechaFragment to plaintext

        :param pecha_fragment: Pecha object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        views_path = []
        spans = pecha_fragment.spans
        base_names = list(spans.keys())
        bases = get_opf_bases(opf_path=pecha_fragment.path, base_names=base_names)
        fragment_id = get_fragment_id()
        for base in bases:
            base_text = base.read_text(encoding="utf-8")
            view_path = output_dir / f"{base.stem}_{fragment_id}.txt"
            view_path.write_text(base_text, encoding="utf-8")
            views_path.append(view_path)
        return views_path


    def serialize_work(self, work: Work, output_dir: Path):
        """
        This function serializes the Work Object based on the type of instances

        :param work: Work object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
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



class PlainTextView(View):
    """
    Class representing Plain Text View

    Attributes
    name: Name of the View
    serializer: Serializer Class
    """

    def __init__(self) -> None:
        self.name = "plaintext"
        self.serializer = PlainTextViewSerializer
        super().__init__(self.name, self.serializer)


    def save_catalog(self, collection_dir: Path, items: List[Item]):
        pass
