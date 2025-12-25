"""src.usecase.eval_item

評価項目（EvalItem）を表すドメインオブジェクトと、ドキュメント表現との相互変換実装を提供します。

EvalItem は `DocConvertible` を継承し、ドキュメント（Markdown）へのレンダリングと、ノード列からの復元を担います。
"""

from src.domain.doc_ir import DocNode, Heading, Table, BulletList
from src.domain.doc_convertible import DocConvertible
from src.domain.markdown_parser import DocParser
from dataclasses import dataclass


@dataclass
class EvalItem(DocConvertible):
    """評価項目を表すデータクラス。

    Attributes:
        id: 評価項目の識別子。
        title: 項目のタイトル。
        eval_type: 種別（例: 機能、性能など）。
        priority: 優先度。
        result: 判定結果。
        conditions: 条件のリスト。
        expected: 期待結果のリスト。
    """

    id: str
    title: str
    eval_type: str
    priority: str
    result: str
    conditions: list[str]
    expected: list[str]

    def to_nodes(self) -> list[DocNode]:
        """EvalItem を `DocNode` 列に変換します（Markdown レンダラ向け）。"""
        return [
            Heading(3, f"{self.id} {self.title}"),
            Table(
                headers=["項目", "内容"],
                rows=[
                    ["種別", self.eval_type],
                    ["優先度", self.priority],
                    ["判定", self.result],
                ],
            ),
            Heading(4, "条件"),
            BulletList(self.conditions),
            Heading(4, "期待結果"),
            BulletList(self.expected),
        ]

    @classmethod
    def from_nodes(cls, nodes: list[DocNode]) -> "EvalItem":
        """ノード列から EvalItem を復元するファクトリメソッド。

        期待するノード構成:
        - レベル3 の見出し: "{id} {title}"
        - 最初に現れる表: 左列がキー、右列が値として読み取る
        - レベル4 の見出し "条件" の直後に箇条書き
        - レベル4 の見出し "期待結果" の直後に箇条書き

        必須要素が欠けている場合は `ValueError` を送出します。
        """
        parser = DocParser(nodes)

        h = parser.first_heading(level=3)
        if h is None:
            raise ValueError("レベル3見出しがありません")

        parts = h.text.split(" ", 1)
        id = parts[0]
        title = parts[1] if len(parts) > 1 else ""

        table = parser.table_as_dict()

        conditions = parser.bullet_list_after("条件", level=4)
        expected = parser.bullet_list_after("期待結果", level=4)

        if not all(
            [id, title, table.get("種別"), table.get("優先度"), table.get("判定")]
        ):
            raise ValueError("EvalItemの必須情報が不足しています")

        return cls(
            id=id,
            title=title,
            eval_type=table["種別"],
            priority=table["優先度"],
            result=table["判定"],
            conditions=conditions,
            expected=expected,
        )
