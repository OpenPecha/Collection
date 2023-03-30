from pydantic import BaseModel
from typing import List,Optional
from collection.items.pecha import Pecha,PechaFragment


class Work(BaseModel):
    id: str
    title: str
    alternative_title: Optional[str]
    bdrc_work_id: str
    authors: List[str]
    best_instance:Optional[Pecha]
    instances: Optional[List[Pecha or PechaFragment]]