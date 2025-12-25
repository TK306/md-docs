"""src.domain.markdown_renderer

`DocNode` から Markdown 文字列を生成するレンダラを提供します。

このモジュールは IR（`DocNode`）を Markdown に変換する責務のみを持ち、整形やファイル入出力は
別責務として扱います。
"""

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
    """
    単一ノードを Markdown 文字列に変換して返します。

    Args:
        node: 変換対象の `DocNode`。

    Returns:
        str: ノードを表す Markdown 文字列（末尾に改行を含む）。
    """
    if isinstance(node, Heading):
        return f"{('#' * node.level)} {node.text}\n"

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


def document_to_markdown(
    doc: Document,
) -> str:
    """
    `Document` を Markdown 文字列に変換して返します。

    前方のフロントマターは HTML コメント形式で出力されます。
    メソッドは文字列変換のみを行い、ファイルの読み書きや整形は呼び出し側で行います。
    """
    out = []

    # front matter as comments
    if doc.front_matter:
        out.append("<!--\n")
        for k, v in doc.front_matter.items():
            out.append(f"{k}: {v}\n")
        out.append("-->\n\n")

    for node in doc.nodes:
        out.append(render_node(node))
        out.append("\n")

    return "".join(out)
