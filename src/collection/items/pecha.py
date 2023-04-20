import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from openpecha.utils import dump_yaml, load_yaml

from collection.items.item import Item
from collection.utils import get_opf_bases


@dataclass
class Pecha(Item):
    id: str
    path: Path
    title: Optional[str] = None
    bdrc_work_id: Optional[str] = None
    bdrc_instance_id: Optional[str] = None

    def serialize(self, serializer, output_dir):
        views_path = serializer.serialize_pecha(self, output_dir)
        return views_path


@dataclass
class PechaFragment(Item):
    """span= {'base':{
    start:0,
    end:10
    }}"""

    id: str
    path: Path
    spans: Dict[str, Dict]
    title: Optional[str] = None
    bdrc_work_id: Optional[str] = None
    bdrc_instance_id: Optional[str] = None

    def __init__(
        self,
        id: str,
        path: Path,
        spans: Dict[str, Dict],
        title: Optional[str] = None,
        bdrc_work_id: Optional[str] = None,
        bdrc_instance_id: Optional[str] = None,
    ):
        self.id = id
        self.path = path
        self.spans = spans
        self.title = title
        self.bdrc_instance_id = bdrc_instance_id
        self.bdrc_work_id = bdrc_work_id
        self.fragment_pecha()

    def serialize(self, serializer, output_dir):
        views_path = serializer.serialize_pecha_fragment(self, output_dir)
        return views_path

    def fragment_pecha(self):
        """
        This function removes the bases and layers not included in pecha fragment from the source opf.
        """
        required_bases = dict(self.spans)
        bases = get_opf_bases(opf_path=self.path)
        for base in bases:
            if base.stem not in required_bases.keys():
                os.remove(base)
        for base_id, span in self.spans.items():
            base_text_path = Path(
                f"{self.path}/{self.path.stem}.opf/base/{base_id}.txt"
            )
            base_text = base_text_path.read_text(encoding="utf-8")
            pagination_layer_path = Path(
                f"{self.path}/{self.path.stem}.opf/layers/{base_id}/pagination.yml"
            )
            pagination_layer = load_yaml(pagination_layer_path)
            new_base_text, new_pagination_layer = self.mod_layer(
                span, base_text, pagination_layer
            )
            dump_yaml(new_pagination_layer, pagination_layer_path)
            base_text_path.write_text(new_base_text, encoding="utf-8")

    def mod_layer(self, span, base_text, pagination_layer):
        """
        This function gives the new base and pagination layer bases on the span.
        :param span: span of the text
        :param base_text: initial base text
        :param pagination_layer: intial pagination layer of the base
        :return base_text: modified base layer
        :return paignation_layer: modified pagination layer
        """
        start = span["start"]
        end = span["end"]
        new_annotations = {}
        annotations = pagination_layer["annotations"]
        total_offset = None
        for ann_id, body in annotations.items():
            body_start = body["span"]["start"]
            body_end = body["span"]["end"]
            is_incld = self.is_span1_included_in_span2(
                (body_start, body_end), (start, end)
            )

            if is_incld:
                if total_offset is None:
                    total_offset = start
                    body["span"]["start"] = 0
                    body["span"]["end"] = body_end - total_offset

                else:
                    body["span"]["start"] = body_start - total_offset
                    body["span"]["end"] = body_end - total_offset

                new_annotations.update({ann_id: body})

        pagination_layer["annotations"] = new_annotations
        base_text = base_text[start:end]
        return base_text, pagination_layer

    def is_span1_included_in_span2(self, span1, span2):
        """
        This function checks if the span1 is included or overlap in span2
        :param span1: span to be checked
        :param span2: pool span where target span is checked
        :return bool: gives boolean on whether the span is included or overlap
        """
        start1, end1 = span1
        start2, end2 = span2
        if start1 <= start2 and end1 >= end2:
            return True
        elif end1 > start2 and end1 < end2:
            return True
        elif start1 < end2 and start1 > start2:
            return True
        else:
            return False
