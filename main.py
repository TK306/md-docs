from pathlib import Path

from src.usecase.document_usecases import dump_eval_item, load_eval_item
from src.usecase.eval_item import EvalItem
from src.adapters.file_storage import FileStorage
from src.adapters.markdown_adapter import MarkdownParserAdapter, MarkdownRendererAdapter


def main() -> None:
    storage = FileStorage()
    parser = MarkdownParserAdapter()
    renderer = MarkdownRendererAdapter()

    item = EvalItem(
        id="E001",
        title="サンプル評価項目",
        eval_type="機能",
        priority="高",
        result="合格",
        conditions=["条件1", "条件2"],
        expected=["期待結果1", "期待結果2"],
    )

    out_path = Path("output.md")
    dump_eval_item(
        item,
        {"title": "評価レポート", "date": "2024-06-15"},
        out_path,
        renderer,
        storage,
    )

    # 読み込み例
    fm, loaded = load_eval_item(Path("input.md"), parser, storage)
    print(f"front_matter={fm}")
    print(loaded)


if __name__ == "__main__":
    main()
