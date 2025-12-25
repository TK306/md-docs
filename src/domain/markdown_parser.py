"""src.domain.markdown_parser

Markdown テキストを `Document`（`DocNode` の列）に変換するパーサを提供します。

このパーサは簡易的な構文解析を行い、見出し、箇条書き、番号リスト、表、画像、段落を
内部表現に変換します。フロントマターは HTML コメント形式（<!-- key: value -->）で読み取ります。
"""

from src.domain.doc_ir import (
    Heading,
    Paragraph,
    BulletList,
    NumberedList,
    Table,
    Image,
    Document,
    DocNode,
)
import re
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


def parse_markdown(markdown_text: str) -> Document:
    """Markdown 文字列をパースして `Document` を返します。

    フロントマターは HTML コメント形式で読み、本文をノード列として返します。

    Raises:
        MarkdownParseError: 構文に問題がある場合に投げられます。
    """
    lines = markdown_text.splitlines()
    front_matter: dict[str, str] = {}
    nodes: list[DocNode] = []
    i = 0

    # Parse front matter from comments
    front_matter = {}
    if i < len(lines) and lines[i].startswith("<!--"):
        i += 1
        while i < len(lines) and not lines[i].startswith("-->"):
            line = lines[i]
            if ":" in line:
                key, value = line.split(":", 1)
                front_matter[key.strip()] = value.strip()
            i += 1
        if i < len(lines):
            i += 1  # Skip -->

    # Skip empty lines after front matter
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Parse body
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            # Heading
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            if not text:
                raise MarkdownParseError(f"Empty heading at line {i + 1}")
            nodes.append(Heading(level, text))
            i += 1
        elif line.startswith("- ") or line.startswith("* "):
            # Bullet list
            items = []
            while i < len(lines) and (
                lines[i].startswith("- ") or lines[i].startswith("* ")
            ):
                items.append(lines[i][2:].strip())
                i += 1
            nodes.append(BulletList(items))
        elif re.match(r"^\d+\.\s", line):
            # Numbered list
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                items.append(re.sub(r"^\d+\.\s", "", lines[i]).strip())
                i += 1
            nodes.append(NumberedList(items))
        elif line.startswith("|"):
            # Table
            headers = [cell.strip() for cell in line.split("|")[1:-1]]
            i += 1
            if i < len(lines) and re.match(r"^\|[\s\-\|]*\|$", lines[i]):
                i += 1  # Skip separator
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                row = [cell.strip() for cell in lines[i].split("|")[1:-1]]
                rows.append(row)
                i += 1
            nodes.append(Table(headers, rows))
        elif line.startswith("!["):
            # Image
            match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if match:
                alt, path = match.groups()
                nodes.append(Image(alt, path))
            else:
                raise MarkdownParseError(f"Invalid image syntax at line {i + 1}")
            i += 1
        elif line.strip():
            # Paragraph
            para_lines = []
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith("#")
                and not lines[i].startswith("- ")
                and not lines[i].startswith("* ")
                and not re.match(r"^\d+\.\s", lines[i])
                and not lines[i].startswith("|")
                and not lines[i].startswith("![")
            ):
                para_lines.append(lines[i])
                i += 1
            text = " ".join(para_lines).strip()
            if text:
                nodes.append(Paragraph(text))
        else:
            i += 1

    return Document(front_matter, nodes)
