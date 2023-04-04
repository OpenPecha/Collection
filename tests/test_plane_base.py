from pathlib import Path
from collection.converter.work_converter import convert_to_work
from collection.items.pecha import Pecha
from collection.views.plain_text import PlainTextViewSerializer

serializer = PlainTextViewSerializer()


def test_pecha_to_plane_base_view():
    
    expected_result = Path("./data/pecha_view_expected_result.txt").read_text(encoding="utf-8")
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
    views_path = serializer.serialize(item=pecha, output_dir=Path("./tests/data"))
    result_view = views_path[0].read_text(encoding="utf-8")
    assert result_view == expected_result

def test_work_to_plane_base_view():
    expected_result = Path("./data/work_view_expected_result.txt").read_text(encoding="utf-8")
    work_path = Path("tests/data/work_sample.yml")
    work = convert_to_work(work_path)
    views_path = serializer.serialize(item=work,output_dir=Path("./tests/data"))
    result_view_path = views_path[0]
    result_view = result_view_path.read_text(encoding="utf-8")
    assert result_view == expected_result


    
