from dataclasses import dataclass
from typing import Dict,Optional
from pathlib import Path

from collection.items.item import Item
from openpecha.utils import load_yaml,dump_yaml
from collection.utils import get_opf_bases

import os

@dataclass
class Pecha(Item):
    id: str
    path: str
    title: Optional[str] = None
    bdrc_work_id: Optional[str] = None
    bdrc_instance_id : Optional[str] = None


@dataclass
class PechaFragment(Item):
    """span= {'base':{
    start:0,
    end:10
    }}"""

    id: str
    path: str
    spans: Dict[str, Dict]
    title: Optional[str] = None
    bdrc_work_id: Optional[str] = None
    bdrc_instance_id: Optional[str] = None
    
    def __init__(self,id:str,path:str,spans:Dict[str, Dict],
                 title:Optional[str] = None,bdrc_work_id:Optional[str] = None,
                 bdrc_instance_id:Optional[str] = None):
        self.id = id
        self.path = path
        self.spans =spans
        self.title = title
        self.bdrc_instance_id = bdrc_instance_id
        self.bdrc_work_id = bdrc_work_id
        self.fragment_pecha()


    def fragment_pecha(self):
        required_bases = dict(self.spans)
        bases = get_opf_bases(opf_path=self.path)
        for base in bases:
            if base.stem not in required_bases.keys():
                os.remove(base)
        for base_id,span in self.spans.items():
            base_text_path = Path(f"{self.path}/{self.path.stem}.opf/base/{base_id}.txt")
            base_text = base_text_path.read_text(encoding="utf-8")
            pagination_layer_path = Path(f"{self.path}/{self.path.stem}.opf/layers/{base_id}/pagination.yml")
            pagination_layer = load_yaml(pagination_layer_path)
            new_base_text,new_pagination_layer = self.mod_layer(span,base_text,pagination_layer)
            dump_yaml(new_pagination_layer,pagination_layer_path)
            base_text_path.write_text(new_base_text,encoding="utf-8")
            


    def mod_layer(self,span,base_text,pagination_layer):
        start = span["start"]
        end = span["end"]
        new_annotations = {}
        annotations = pagination_layer["annotations"]
        for ann_id,body in annotations.items():
            body_start = body["span"]["start"]
            body_end = body["span"]["end"]
            is_incld = self.is_span1_included_in_span2((body_start,body_end),(start,end))
            if is_incld:
                new_annotations.update({ann_id:body})
        pagination_layer["annotations"] = new_annotations
        base_text = base_text[start:end]
        return base_text,pagination_layer


    def is_span1_included_in_span2(self,span1,span2):
        start1, end1 = span1
        start2, end2 = span2
        if start1 <= start2 and end1 >= end2:
            return True
        elif end1 > start2 and end1 < end2 :
            return True
        elif start1 < end2 and start1 > start2:
            return True
        else:
            return False


