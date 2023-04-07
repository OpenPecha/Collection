from pydantic import BaseModel
from typing import Dict



class CollectionMeta(BaseModel):
    collection_id:str
    item_views_map:Dict