"""src.adapters.markdown_renderer

`Document` を Markdown 文字列に変換する実装（adapters 層）。
"""

from src.domain.doc_ir import (
    Document,
    Heading,
    Paragraph,
    BulletList,
    NumberedList,
    Table,
    Image,
)


def document_to_markdown(doc: Document) -> str:
    out = []

    # front matter as comments
    if doc.front_matter:
        out.append("<!--\n")
        for k, v in doc.front_matter.items():
            out.append(f"{k}: {v}\n")
        out.append("-->\n\n")

    for node in doc.nodes:
        if isinstance(node, Heading):
            out.append(f"{('#' * node.level)} {node.text}\n")
        elif isinstance(node, Paragraph):
            out.append(f"{node.text}\n")
        elif isinstance(node, BulletList):
            out.append("".join(f"- {item}\n" for item in node.items))
        elif isinstance(node, NumberedList):
            out.append(
                "".join(f"{i + 1}. {item}\n" for i, item in enumerate(node.items))
            )
        elif isinstance(node, Table):
            header = "| " + " | ".join(node.headers) + " |\n"
            sep = "| " + " | ".join(["----"] * len(node.headers)) + " |\n"
            rows = "".join("| " + " | ".join(r) + " |\n" for r in node.rows)
            out.append(header + sep + rows)
        elif isinstance(node, Image):
            out.append(f"![{node.alt}]({node.path})\n")
        else:
            raise TypeError(node)

        out.append("\n")

    return "".join(out)
