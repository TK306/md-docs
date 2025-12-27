import pytest

from src.usecase.eval_item import EvalItem
from src.domain.doc_ir import Heading, Table


def test_evalitem_from_nodes_missing_required_keys_raises():
    # '判定' が欠けている（必須キー）
    nodes = [
        Heading(3, "T001 タイトル"),
        Table(headers=["項目", "内容"], rows=[["種別", "機能"], ["優先度", "高"]]),
    ]
    with pytest.raises(ValueError):
        EvalItem.from_nodes(nodes)


def test_evalitem_from_nodes_missing_table_raises():
    # 表自体が無い場合もエラーになる
    nodes = [Heading(3, "T002 タイトル")]
    with pytest.raises(ValueError):
        EvalItem.from_nodes(nodes)
