from pathlib import Path

from src.usecase.document_usecases import dump_eval_item, load_eval_item
from src.usecase.eval_item import EvalItem
from src.adapters.file_storage import FileStorage
from src.adapters.markdown_adapter import MarkdownParserAdapter, MarkdownRendererAdapter


def test_dump_and_load_eval_item(tmp_path: Path):
    storage = FileStorage()
    parser = MarkdownParserAdapter()
    renderer = MarkdownRendererAdapter()

    item = EvalItem(
        id="T001",
        title="テスト項目",
        eval_type="機能",
        priority="中",
        result="未実施",
        conditions=["c1", "c2"],
        expected=["e1"],
    )

    fm = {"title": "テスト", "date": "2025-01-01"}
    out_file = tmp_path / "test.md"

    # dump
    dump_eval_item(item, fm, out_file, renderer, storage)

    # load
    loaded_fm, loaded_item = load_eval_item(out_file, parser, storage)

    assert loaded_fm["title"] == fm["title"]
    assert loaded_item.id == item.id
    assert loaded_item.title == item.title
    assert loaded_item.eval_type == item.eval_type
    assert loaded_item.priority == item.priority
    assert loaded_item.conditions == item.conditions
    assert loaded_item.expected == item.expected
