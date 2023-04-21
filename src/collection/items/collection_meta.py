from typing import Dict

from pydantic import BaseModel


class CollectionMeta(BaseModel):
    collection_id: str
    item_views_map: Dict
