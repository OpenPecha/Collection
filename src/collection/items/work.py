from typing import List, Optional, Union,Dict
from pathlib import Path

from pydantic import BaseModel

from openpecha.utils import load_yaml

from collection.items.pecha import Pecha, PechaFragment
from collection.utils import get_item


class Work(BaseModel):
    id: str
    title: str
    alternative_title: Optional[str]
    bdrc_work_id: str
    authors: List[str]
    best_instance: Optional[Pecha]
    instances: Optional[List[Union[Pecha, PechaFragment]]]

    def __init__(self, work_file:Path) -> None:
        work = get_work(work_file)
        super().__init__(**work)

    class Config:
        arbitrary_types_allowed = True
    
    def serialize(self,serializer,output_dir):
        views_path = serializer.serialize_work(self,output_dir)
        return views_path


def get_obj(instance, cls, bdrc_work_id):
    if instance["id"] is None:
        return
    new_attrs = {}
    attrs = cls.__annotations__.keys()
    for attr in attrs:
        if attr == "bdrc_work_id":
            new_attrs.update({attr: bdrc_work_id})
        elif attr in instance.keys():
            new_attrs.update({attr: instance[attr]})

    
    path = get_item(instance["id"])
    new_attrs.update({"path": Path(path)})
    obj = cls(**new_attrs)
    return obj


def convert_to_instance(instance, bdrc_work_id):
    """
    This function converts the dictionary of string instance to Instance obj

    :param instance: dictioinary of a instance
    :param bdrc_work_id: BDRC work id
    :return: echa or PechaFragment object
    """
    if "spans" not in instance.keys() or instance["spans"] is None:
        return get_obj(instance, Pecha, bdrc_work_id)
    else:
        return get_obj(instance, PechaFragment, bdrc_work_id)


def get_instances(work_file):
    """
    This function returns the instance obj

    :param work_file: Path obj of work file
    :return: Pecha or PechaFragment objects
    """
    objs = []
    instances = work_file["instances"]
    if instances is None:
        return

    for instance in instances:
        obj = convert_to_instance(instance, work_file["bdrc_work_id"])
        if obj:
            objs.append(obj)
    return objs


def get_work_dic(work_file: Dict, instance_objs):
    """
    This function converts the work file to Work dic will all the attributes

    :param work_file: Dictioniary of Work
    :param instance_objs: Instance objs of the work
    :return: Work obj
    """
    work_dic = {}
    attrs = Work.__annotations__.keys()
    for attr in attrs:
        if attr == "instances":
            continue
        elif attr == "id":
            work_dic.update({attr:work_file["id"]})
        else:
            work_dic.update({attr: work_file[attr]})
    work_dic.update({"instances": instance_objs})
    return work_dic


def get_work(work_file: Path):
    """
    This function returns the work obj when a workfile is given

    :param work_file: Path obj of work file
    :return: Work obj
    """
    work_dic = load_yaml(work_file)
    instance_objs = get_instances(work_dic)
    work_dic = get_work_dic(work_dic, instance_objs)
    return work_dic
