from pathlib import Path
from typing import Dict

from openpecha.utils import load_yaml

from collection.items.pecha import Pecha, PechaFragment
from collection.items.work import Work
from collection.utils import get_item


def get_obj(instance, cls, bdrc_work_id):
    new_attrs = {}
    attrs = cls.__annotations__.keys()
    for attr in attrs:
        if attr == "bdrc_work_id":
            new_attrs.update({attr: bdrc_work_id})
        elif attr in instance.keys():
            new_attrs.update({attr: instance[attr]})

    path = get_item(instance["id"])
    new_attrs.update({"path": path})
    obj = cls(**new_attrs)
    return obj


def convert_to_instance(instance, bdrc_work_id):
    if "spans" not in instance.keys() or instance["spans"] is None:
        obj = get_obj(instance, Pecha, bdrc_work_id)
    else:
        obj = get_obj(instance, PechaFragment, bdrc_work_id)

    return obj


def get_instances(work_file):
    objs = []
    instances = work_file["instances"]
    if instances is None:
        return

    for instance in instances:
        obj = convert_to_instance(instance, work_file["bdrc_work_id"])
        objs.append(obj)
    return objs


def get_work_obj(work_file: Dict, instance_objs):
    new_attrs = {}
    attrs = Work.__annotations__.keys()
    for attr in attrs:
        if attr == "instances":
            continue
        new_attrs.update({attr: work_file[attr]})
    new_attrs.update({"instances": instance_objs})
    obj = Work(**new_attrs)
    return obj


def convert_to_work(work_file: Path):
    work_dic = load_yaml(work_file)
    instance_objs = get_instances(work_dic)
    work_obj = get_work_obj(work_dic, instance_objs)
    return work_obj
