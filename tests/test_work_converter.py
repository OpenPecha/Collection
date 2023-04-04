import shutil
from pathlib import Path

from openpecha.utils import load_yaml

from collection.converter.work_converter import convert_to_instance, convert_to_work
from collection.items.work import Pecha, Work


def test_convert_to_intance():
    work_file = load_yaml(Path("./tests/data/test_work.yml"))
    instances = work_file["instances"]
    instance = instances[0]
    result_instance = convert_to_instance(bdrc_work_id="WA0RT0010", instance=instance)
    expected_instance = Pecha(
        id="I9D4B6344",
        title="དྷརྨ་དྷ་ཏུ་སྟ་པ།",
        bdrc_work_id="WA0RT0010",
        path="/home/runner/.openpecha/I9D4B6344",
    )
    print(expected_instance)
    print(result_instance)
    assert expected_instance == result_instance
    shutil.rmtree("/home/runner/.openpecha/")


def test_convert_to_work():
    result_work = convert_to_work(Path("./tests/data/test_work.yml"))
    result_work.instances = None
    expected_work = Work(
        id="W8D2C5ECC",
        title="ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ།",
        alternative_title="དྷརྨདྷāཏུསྟབ༹",
        bdrc_work_id="WA0RT0010",
        authors=["龙树"],
    )
    print(expected_work)
    print(result_work)
    assert expected_work == result_work
