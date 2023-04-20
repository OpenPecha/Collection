import shutil
from pathlib import Path

from openpecha.utils import load_yaml

from collection.items.work import Pecha, convert_to_instance, get_work,PechaFragment


def test_convert_to_intance():
    work_file = load_yaml(Path("tests/data/work_sample.yml"))
    instances = work_file["instances"]
    instance = instances[0]
    result_instance = convert_to_instance(bdrc_work_id="WA0RT0010", instance=instance)
    print(result_instance)
    expected_instance = PechaFragment(
        id="I3D4F1804",
        path=Path("/home/runner/.openpecha/I3D4F1804"),
        spans={"I3CN3916":
               {"start":0,
                "end":100}},
        title="དྷརྨ་དྷ་ཏུ་སྟ་པ།",
        bdrc_work_id="WA0RT0010",
        bdrc_instance_id=None
    )
    
    print(expected_instance)
    print(result_instance)
    assert expected_instance == result_instance
    shutil.rmtree("/home/runner/.openpecha/")


def test_convert_to_work():
    result_work = get_work(Path("tests/data/work_sample.yml"))
    result_work["instances"] = None
    expected_work = {
        "id": "W8D2C5ECC",
        "title": "ཆོས་ཀྱི་དབྱིངས་སུ་བསྟོད་པ།",
        "alternative_title": "དྷརྨདྷāཏུསྟབ༹",
        "bdrc_work_id": "WA0RT0010",
        "authors": ["龙树","ནག་ཚོ་ལོ་ཙཱ་བ།"],
        "best_instance": None,
        "instances": None,
    }
    print(expected_work)
    print(result_work)
    assert expected_work == result_work
