from pathlib import Path
from typing import List

from collection.items.item import Item
from collection.items.pecha import Pecha
from collection.views.view import View, ViewSerializer


def get_opf_bases(opf_path: str):
    bases = []
    pecha_id = Path(opf_path).stem
    bases = list(Path(f"{opf_path}/{pecha_id}.opf/base").iterdir())
    return bases


class PlainBaseViewSerializer(ViewSerializer):
    def serialize(self, pecha: Pecha, output_dir: Path):
        views_path = []
        base_names = get_opf_bases(pecha.path)
        for base_name in base_names:
            base_text = base_name.read_text(encoding="utf-8")
            Path(f"{output_dir}/{base_name.name}").write_text(
                base_text, encoding="utf-8"
            )
            views_path.append(Path(f"{output_dir}/{base_name.name}"))
        return views_path


class PlainBaseView(View):
    def __init__(self) -> None:
        name = "PlainBaseView"
        serializer = PlainBaseViewSerializer
        super().__init__(name, serializer)

    def serialize(self, pecha: Pecha, output_dir: Path):
        views_path = self.serializer_class().serialize(pecha, output_dir)
        return views_path

    def save_catalog(self, collection_dir: Path, items: List[Item]):
        pass
