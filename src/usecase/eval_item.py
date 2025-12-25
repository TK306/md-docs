from src.domain.doc_ir import DocNode, Heading, Table, BulletList
from dataclasses import dataclass


@dataclass
class EvalItem:
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
