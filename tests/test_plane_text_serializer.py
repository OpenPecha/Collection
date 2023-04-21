from pathlib import Path

from collection.items.pecha import Pecha
from collection.items.work import Work
from collection.views.plain_text import PlainTextViewSerializer

serializer = PlainTextViewSerializer()


def test_pecha_to_plane_text():
    expected_result = Path("tests/data/expected_pecha_plaintext.txt").read_text(
        encoding="utf-8"
    )
    pecha_path = Path("./tests/data/I3D4F1804")
    id = "I3D4F1804"
    title = ""
    bdrc_id = ""
    pecha = Pecha(
        id=id,
        title=title,
        path=pecha_path,
        bdrc_work_id=bdrc_id,
    )
    views_path = pecha.serialize(serializer, output_dir=Path("./tests/data"))
    result_view = views_path[0].read_text(encoding="utf-8")
    assert result_view == expected_result


def test_work_to_plane_text():
    expected_result = Path("tests/data/expected_work_plaintext.txt").read_text(
        encoding="utf-8"
    )
    work_path = Path("tests/data/work_sample.yml")
    work = Work(work_path)
    views_path = work.serialize(serializer, output_dir=Path("./tests/data"))
    result_view_path = views_path[0]
    result_view = result_view_path.read_text(encoding="utf-8")
    assert result_view == expected_result
