import csv
from pathlib import Path
from typing import List
from collection.items.pecha import Pecha
from collection.views.view import View, ViewSerializer


def get_opf_bases(opf_path:str):
    bases = []
    pecha_id = Path(opf_path).stem
    bases = list(Path(f"{opf_path}/{pecha_id}.opf/base").iterdir())
    return bases



class PlainBaseViewSerializer(ViewSerializer):

    @classmethod
    def serialize(self, pecha: Pecha, output_dir: Path):
        views_path = []
        base_names = get_opf_bases(pecha.pecha_path)
        for base_name in base_names:
            base_text = base_name.read_text(encoding="utf-8")
            Path(f"{output_dir}/{base_name.name}").write_text(base_text, encoding='utf-8')
            views_path.append( Path(f"{output_dir}/{base_name.name}"))
        return views_path
    

class PlainBaseView(View):
    def __init__(self) -> None:
        name = "PlainBaseView"
        serializer= PlainBaseViewSerializer
        super().__init__(name, serializer)

    def serialize(self, pecha: Pecha, output_dir: Path):
        views_path = self.serializer_class.serialize(pecha,output_dir)
        return views_path

    def save_catalog(self, collection_dir: Path, items: List[Pecha]):
        catalog_file_path = collection_dir / f"Catalog_{self.name}.csv"
        field_names = ['FILE NAME', 'TITLE', 'OP ID', 'BDRC ID', 'VOLUME NUMBER']
        items = []
        for item in items:
            cur_item_infos = [
                item.base_name,
                item.title,
                item.id,
                item.bdrc_id,
                item.volume_number
            ]
            items.append(cur_item_infos)
        with open(catalog_file_path, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)   
            csvwriter.writerow(field_names) 
        
            # writing the data rows 
            csvwriter.writerows(items)
        
