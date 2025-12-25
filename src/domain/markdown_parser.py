"""src.domain.markdown_parser

Markdown テキストを `Document`（`DocNode` の列）に変換するパーサを提供します。

このパーサは簡易的な構文解析を行い、見出し、箇条書き、番号リスト、表、画像、段落を
内部表現に変換します。フロントマターは HTML コメント形式（<!-- key: value -->）で読み取ります。
"""

from src.domain.doc_ir import (
    Heading,
    BulletList,
    Table,
    DocNode,
)
from typing import cast


class MarkdownParseError(Exception):
    """Markdown の構文が期待どおりでない場合に投げられる例外。"""


class DocParser:
    """`Document.nodes` を操作するためのユーティリティクラス。

    目的は、パース済みノード列から見出しや表、箇条書きなどを簡単に検索・取得することです。
    """

    def __init__(self, nodes: list[DocNode]):
        """ノード列で初期化します。"""
        self.nodes = nodes

    def find_heading(self, level: int) -> list[Heading]:
        """指定レベルの見出しをすべて返します。"""
        return [n for n in self.nodes if isinstance(n, Heading) and n.level == level]

    def first_heading(self, level: int) -> Heading | None:
        """指定レベルの最初の見出しを返します。存在しなければ None を返します。"""
        for n in self.nodes:
            if isinstance(n, Heading) and n.level == level:
                return n
        return None

    def table_as_dict(self) -> dict[str, str]:
        """最初に見つかった表を辞書（左列をキー、右列を値）として返します。"""
        for n in self.nodes:
            if isinstance(n, Table):
                return {row[0]: row[1] for row in cast(Table, n).rows if len(row) >= 2}
        return {}

    def bullet_list_after(self, heading_text: str, level: int) -> list[str]:
        """指定の見出しテキストの直後にある箇条書きを返します。なければ空リスト。"""
        for i, n in enumerate(self.nodes):
            if (
                isinstance(n, Heading)
                and n.level == level
                and n.text == heading_text
                and i + 1 < len(self.nodes)
                and isinstance(self.nodes[i + 1], BulletList)
            ):
                return cast(BulletList, self.nodes[i + 1]).items
        return []
