from pathlib import Path
from typing import Dict

from openpecha.utils import load_yaml

from collection.items.pecha import Pecha, PechaFragment
from collection.items.work import Work
from collection.utils import get_item


def get_obj(instance, cls, bdrc_work_id):
    if instance["op_id"] is None:
        return
    new_attrs = {}
    attrs = cls.__annotations__.keys()
    for attr in attrs:
        if attr == "bdrc_work_id":
            new_attrs.update({attr: bdrc_work_id})
        elif attr in instance.keys():
            new_attrs.update({attr: instance[attr]})

    
    path = get_item(instance["op_id"])
    new_attrs.update({"path": path})
    obj = cls(**new_attrs)
    return obj


def convert_to_instance(instance, bdrc_work_id):
    """
    This function converts the dictionary of instance to Instance obj

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


def get_work_obj(work_file: Dict, instance_objs):
    """
    This function converst the work file to Work obj

    :param work_file: Dictioniary of Work
    :param instance_objs: Instance objs of the work
    :return: Work obj
    """
    new_attrs = {}
    attrs = Work.__annotations__.keys()
    for attr in attrs:
        if attr == "instances":
            continue
        elif attr == "id":
            new_attrs.update({attr:work_file["op_id"]})
        else:
            new_attrs.update({attr: work_file[attr]})
    new_attrs.update({"instances": instance_objs})
    obj = Work(**new_attrs)
    return obj


def convert_to_work(work_file: Path):
    """
    This function returns the work obj when a workfile is given

    :param work_file: Path obj of work file
    :return: Work obj
    """
    work_dic = load_yaml(work_file)
    instance_objs = get_instances(work_dic)
    work_obj = get_work_obj(work_dic, instance_objs)
    return work_obj
