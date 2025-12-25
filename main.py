from src.usecase.eval_item import EvalItem
from pathlib import Path

item = EvalItem(
    id="E001",
    title="サンプル評価項目",
    eval_type="機能",
    priority="高",
    result="合格",
    conditions=["条件1", "条件2"],
    expected=["期待結果1", "期待結果2"],
)


item.dump_markdown({"title": "評価レポート", "date": "2024-06-15"}, Path("output.md"))

front_matter, item = EvalItem.load_markdown(Path("input.md"))

print(item)
