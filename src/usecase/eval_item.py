from src.domain.doc_ir import DocNode, Heading, Table, BulletList
from dataclasses import dataclass
from typing import cast


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

    @staticmethod
    def from_nodes(nodes: list[DocNode]) -> "EvalItem":
        id = ""
        title = ""
        eval_type = ""
        priority = ""
        result = ""
        conditions: list[str] = []
        expected: list[str] = []

        i = 0
        while i < len(nodes):
            node = nodes[i]
            if isinstance(node, Heading) and node.level == 3:
                parts = node.text.split(" ", 1)
                id = parts[0]
                title = parts[1] if len(parts) > 1 else ""
            elif isinstance(node, Table):
                for row in node.rows:
                    if row[0] == "種別":
                        eval_type = row[1]
                    elif row[0] == "優先度":
                        priority = row[1]
                    elif row[0] == "判定":
                        result = row[1]
            elif isinstance(node, Heading) and node.level == 4:
                if (
                    node.text == "条件"
                    and i + 1 < len(nodes)
                    and isinstance(nodes[i + 1], BulletList)
                ):
                    conditions = cast(BulletList, nodes[i + 1]).items
                    i += 1
                elif (
                    node.text == "期待結果"
                    and i + 1 < len(nodes)
                    and isinstance(nodes[i + 1], BulletList)
                ):
                    expected = cast(BulletList, nodes[i + 1]).items
                    i += 1
            i += 1

        return EvalItem(
            id=id,
            title=title,
            eval_type=eval_type,
            priority=priority,
            result=result,
            conditions=conditions,
            expected=expected,
        )
