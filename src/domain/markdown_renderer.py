from src.domain.doc_ir import (
    Heading,
    Paragraph,
    BulletList,
    NumberedList,
    Table,
    Image,
    DocNode,
    Document,
)


def render_node(node: DocNode) -> str:
    if isinstance(node, Heading):
        return f"{'#' * node.level} {node.text}\n"

    if isinstance(node, Paragraph):
        return f"{node.text}\n"

    if isinstance(node, BulletList):
        return "".join(f"- {item}\n" for item in node.items)

    if isinstance(node, NumberedList):
        return "".join(f"{i + 1}. {item}\n" for i, item in enumerate(node.items))

    if isinstance(node, Table):
        header = "| " + " | ".join(node.headers) + " |\n"
        sep = "| " + " | ".join(["----"] * len(node.headers)) + " |\n"
        rows = "".join("| " + " | ".join(r) + " |\n" for r in node.rows)
        return header + sep + rows

    if isinstance(node, Image):
        return f"![{node.alt}]({node.path})\n"

    raise TypeError(node)


def document_to_markdown(doc: Document) -> str:
    out = []

    # front matter
    out.append("---\n")
    for k, v in doc.front_matter.items():
        out.append(f"{k}: {v}\n")
    out.append("---\n\n")

    for node in doc.nodes:
        out.append(render_node(node))
        out.append("\n")

    return "".join(out)
