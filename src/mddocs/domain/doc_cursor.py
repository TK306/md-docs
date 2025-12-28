"""src.domain.doc_cursor

ノード列を順次巡回するユーティリティ。

DocConvertible の具象実装を簡潔にするための小さな API を提供します。
"""

from __future__ import annotations

from typing import Callable, List, Optional, TypeVar, Type, cast

from mddocs.domain.doc_ir import DocNode, Paragraph, Table


T = TypeVar("T", bound=DocNode)


class NodeCursor:
    """ノード列を順に読み進める軽量カーソル。

    ノードは破壊的に消費される（`index` が進む）。必要なら `fork()` でコピーを取得できます。
    """

    def __init__(
        self, nodes: List[DocNode], front_matter: Optional[dict] = None
    ) -> None:
        self.front_matter: dict = front_matter or {}
        self.nodes: List[DocNode] = list(nodes)
        self.index: int = 0

    @property
    def done(self) -> bool:
        return self.index >= len(self.nodes)

    def peek(self) -> Optional[DocNode]:
        """現在位置のノードを返す（進めない）。存在しなければ `None` を返す。"""
        if self.done:
            return None
        return self.nodes[self.index]

    def next(self) -> DocNode:
        """現在のノードを返してカーソルを進める。末尾で `StopIteration` を送出する。"""
        if self.done:
            raise StopIteration()
        node = self.nodes[self.index]
        self.index += 1
        return node

    def expect(self, node_type: Type[T]) -> T:
        """現在のノードが `node_type` のインスタンスであればそれを消費して返す。

        そうでなければ `ValueError` を送出する。
        """
        node = self.peek()
        if node is None or not isinstance(node, node_type):
            raise ValueError(
                f"NodeCursor.expect: expected {node_type.__name__}, got {type(node).__name__ if node is not None else 'EOF'}"
            )
        return cast(T, self.next())

    def take_while(self, predicate: Callable[[DocNode], bool]) -> List[DocNode]:
        """predicate が True の間ノードを消費してリストで返す。"""
        out: List[DocNode] = []
        while not self.done:
            p = self.peek()
            if p is None or not predicate(p):
                break
            out.append(self.next())
        return out

    def collect_paragraph_text(self) -> str:
        """連続する `Paragraph` ノードをまとめてテキストにして返す。"""
        paras = self.take_while(lambda n: isinstance(n, Paragraph))
        # mypy cannot infer that items are Paragraph, so cast for attribute access
        return "\n\n".join(cast(Paragraph, p).text for p in paras)

    def parse_table_as_dict(self, ignore_extra_columns: bool = False) -> dict:
        """現在のノードが `Table` のとき `Table.as_dict()` を返す（`expect` を使用）。"""
        table = self.expect(Table)
        return table.as_dict(ignore_extra_columns=ignore_extra_columns)

    def fork(self) -> "NodeCursor":
        """現在位置から fork した新しいカーソルを返す（浅いコピー）。"""
        return NodeCursor(self.nodes[self.index :], dict(self.front_matter))

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<NodeCursor index={self.index} len={len(self.nodes)}>"
