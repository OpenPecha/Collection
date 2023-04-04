from pathlib import Path

from collection.items.pecha import Pecha
from collection.views.plain_text import PlainBaseViewSerializer

serializer = PlainBaseViewSerializer()


def test_plane_base_view_serializer():
    expected_result = Path("tests/data/expected_result.txt").read_text(encoding="utf-8")
    pecha_path = "./tests/data/I3D4F1804"
    id = "I3D4F1804"
    title = ""
    bdrc_id = ""
    pecha = Pecha(
        id=id,
        title=title,
        path=pecha_path,
        bdrc_work_id=bdrc_id,
    )
    views_path = serializer.serialize(pecha=pecha, output_dir=Path("./tests/data"))
    result_view = views_path[0].read_text(encoding="utf-8")
    assert result_view == expected_result
