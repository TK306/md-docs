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


class MarkdownParseError(Exception):
    pass


def parse_markdown(markdown_text: str) -> Document:
    """
    Parse markdown text into a Document structure.
    Raises MarkdownParseError if parsing fails.
    """
    lines = markdown_text.splitlines()
    front_matter = {}
    nodes: list[DocNode] = []
    i = 0

    # Parse front matter
    if lines and lines[0] == "---":
        i = 1
        while i < len(lines) and lines[i] != "---":
            if ":" in lines[i]:
                key, value = lines[i].split(":", 1)
                front_matter[key.strip()] = value.strip()
            i += 1
        i += 1  # Skip the closing ---

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
