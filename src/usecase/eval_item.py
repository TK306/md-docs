from src.domain.doc_ir import DocNode, Heading, Table, BulletList
from src.domain.doc_convertible import DocConvertible
from src.domain.markdown_parser import DocParser
from dataclasses import dataclass


@dataclass
class EvalItem(DocConvertible):
    id: str
    title: str
    eval_type: str
    priority: str
    result: str
    conditions: list[str]
    expected: list[str]

    def to_nodes(self) -> list[DocNode]:
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
