from pathlib import Path

from src.usecase.document_usecases import dump_eval_item, load_eval_item
from src.usecase.eval_item import EvalItem
from src.adapters.file_storage import FileStorage
from src.adapters.markdown_adapter import MarkdownParserAdapter, MarkdownRendererAdapter


# このテストはユースケース層を通じてファイルに EvalItem を書き出し、
# 同じファイルを読み戻して元のオブジェクトと一致することを検証します。
# 具体的には以下を確認します:
# - ユースケースが storage と renderer/parser を正しく呼び出すこと
# - フロントマターが保持されること
# - EvalItem のフィールドが round-trip（dump -> load）で一致すること
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

    # dump: ユースケース経由で EvalItem を Markdown にレンダリングしてファイルに書き出す
    dump_eval_item(item, fm, out_file, renderer, storage)

    # load: ファイルを読み込み、パースして EvalItem に復元する
    loaded_fm, loaded_item = load_eval_item(out_file, parser, storage)

    # フロントマターが期待どおりに保持されている
    assert loaded_fm["title"] == fm["title"]

    # EvalItem の各フィールドが round-trip で一致する
    assert loaded_item.id == item.id
    assert loaded_item.title == item.title
    assert loaded_item.eval_type == item.eval_type
    assert loaded_item.priority == item.priority
    assert loaded_item.conditions == item.conditions
    assert loaded_item.expected == item.expected
