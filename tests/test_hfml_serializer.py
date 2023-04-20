from pathlib import Path

from collection.items.pecha import Pecha
from collection.views.hfml import HFMLViewSerializer
from collection.items.work import Work

serializer = HFMLViewSerializer()

def test_work_to_hfml():
    expected_result = Path("tests/data/expected_work_hfml.txt").read_text(
        encoding="utf-8"
    )
    work_path = Path("tests/data/work_sample.yml")
    work = Work(work_path)
    views_path = work.serialize(serializer, output_dir=Path("./tests/data"))
    result_view_path = views_path[0]
    result_view = result_view_path.read_text(encoding="utf-8")
    assert result_view == expected_result



def test_pecha_to_hfml():
    expected_result = Path("tests/data/expected_pecha_hfml.txt").read_text(
        encoding="utf-8"
    )
    pecha_path = "./tests/data/I3D4F1804"
    id = "I3D4F1804"
    title = "demo"
    pecha = Pecha(
        id=id,
        path=pecha_path,
    )
    views_path = pecha.serialize(serializer, output_dir=Path("./tests/data"))
    result_view = views_path[0].read_text(encoding="utf-8")
    assert result_view == expected_result