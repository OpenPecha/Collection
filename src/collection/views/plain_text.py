import uuid
from pathlib import Path
from typing import List

from collection.items.item import Item
from collection.items.pecha import Pecha, PechaFragment
from collection.items.work import Work
from collection.views.view import View, ViewSerializer


class PlainTextViewSerializer(ViewSerializer):
    """
    Class represeting the PlainText View Serializer

    """

    def serialize(self, item: Item, output_dir: Path):
        """
        This function calls the particular serializer based on item

        :param item: Item to be serialize
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        if isinstance(item, Pecha):
            view_paths = self.serialize_pecha(item, output_dir)
        elif isinstance(item, Work):
            view_paths = self.serialize_work(item, output_dir)
        else:
            raise ValueError(f"{item} serializer not supported for PlainTextView")
        view_names = [view_path.name for view_path in view_paths]
        item_views_map = {item.id:view_names}
        return item_views_map

    def serialize_pecha(self, pecha: Pecha, output_dir: Path):
        """
        This function serializes the Pecha object

        :param pecha: Pecha object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        views_path = []
        bases = self.get_opf_bases(pecha.path)
        for base in bases:
            base_text = base.read_text(encoding="utf-8")
            view_path = output_dir / f"{base.name}"
            view_path.write_text(base_text, encoding="utf-8")
            views_path.append(view_path)
        return views_path

    def serialize_pechaFragment(self, pecha_fragment: PechaFragment, output_dir: Path):
        """
        This function serializes the PechaFragment object

        :param pecha_fragment: Pecha object
        :outputdir: Directory to save the view
        :return: List of view paths in Path object
        """
        views_path = []
        spans = pecha_fragment.spans
        base_names = list(spans.keys())
        bases = self.get_opf_bases(opf_path=pecha_fragment.path, base_names=base_names)
        fragment_id = self.get_fragment_id()
        for base in bases:
            span = spans[base.stem]
            base_text = base.read_text(encoding="utf-8")
            view_path = output_dir / f"{base.stem}_{fragment_id}.txt"
            fragment_text = base_text[span["start"]:span["end"]]
            view_path.write_text(fragment_text, encoding="utf-8")
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
                views_path = self.serialize_pechaFragment(instance, output_dir)
            else:
                raise ValueError(f"{instance} Not a Valid Work Instance")
            views_paths.extend(views_path)

        return views_paths

    @staticmethod
    def get_opf_bases(opf_path: str, base_names: List = None):
        """
        This function gives the bases of a given opf or path of bases

        :param opf_path: path of opf
        :base_names: List of Base names
        :return: list of bases path in Path obj
        """
        pecha_id = Path(opf_path).stem
        bases = list(Path(f"{opf_path}/{pecha_id}.opf/base").iterdir())
        ret_bases = []
        if base_names:
            for base in bases:
                if base.stem in base_names:
                    ret_bases.append(base)
        else:
            ret_bases = bases
        return ret_bases

    @staticmethod
    def get_fragment_id():
        return uuid.uuid4().hex[:4]


class PlainTextView(View):
    """
    Class representing Plain text view

    Attributes
    name: Name of the View
    serializer: Serializer Class
    """

    def __init__(self) -> None:
        self.name = "PlainTextView"
        self.serializer = PlainTextViewSerializer
        super().__init__(self.name, self.serializer)

    def save_catalog(self, collection_dir: Path, items: List[Item]):
        pass
