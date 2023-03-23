from collection.views.plain_base import PlainBaseViewSerializer
from collection.items.pecha import PechaMeta
from pathlib import Path

serializer = PlainBaseViewSerializer()


def test_plane_base_view_serializer():
    expected_result = Path("tests/data/expected_result.txt").read_text(encoding="utf-8")
    pecha_path = "./tests/data/I3D4F1804"
    id = "I3D4F1804"
    title = ""
    bdrc_id =""
    volume_number=1
    base_name = ""
    pecha = PechaMeta(
        id=id,
        title=title,
        volume_number=volume_number,
        base_name=base_name,
        pecha_path=pecha_path,
        bdrc_id=bdrc_id
    )
    views_path = serializer.serialize(pecha=pecha,output_dir="./tests/data")
    result_view = views_path[0].read_text(encoding= "utf-8")
    assert result_view == expected_result