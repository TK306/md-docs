"""src.adapters.markdown_parser

Markdown テキストを `Document`（`DocNode` の列）に変換する実装。

`DocParser`（domain）とは別に、ファイル/文字列を `Document` に変換する責務をここに置きます。
"""

from src.domain.doc_ir import (
    Document,
    DocNode,
    Heading,
    Paragraph,
    BulletList,
    NumberedList,
    Table,
    Image,
)
from src.domain.markdown_parser import MarkdownParseError
import re


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
