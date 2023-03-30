from typing import List, Optional, Union

from pydantic import BaseModel

from collection.items.pecha import Pecha, PechaFragment


class Work(BaseModel):
    id: str
    title: str
    alternative_title: Optional[str]
    bdrc_work_id: str
    authors: List[str]
    best_instance: Optional[Pecha]
    instances: Optional[List[Union[Pecha, PechaFragment]]]
