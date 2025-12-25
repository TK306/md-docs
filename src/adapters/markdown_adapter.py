"""src.adapters.markdown_adapter

`DocumentParser` / `DocumentRenderer` の具体実装ラッパー。
内部で既存の `parse_markdown` / `document_to_markdown` を呼び出し、必要に応じて
追加の整形（`mdformat`）を行います。
"""

from __future__ import annotations

from src.interfaces.protocols import DocumentParser, DocumentRenderer
from src.adapters.markdown_parser import parse_markdown
from src.adapters.markdown_renderer import document_to_markdown
import mdformat


class MarkdownParserAdapter(DocumentParser):
    """既存の `parse_markdown` を DocumentParser プロトコルに適合させるアダプタ。"""

    def parse(self, text: str):
        # パース前に整形は行わず、parse_markdown に渡す
        return parse_markdown(text)


class MarkdownRendererAdapter(DocumentRenderer):
    """`document_to_markdown` をラップし、出力時に `mdformat` で整形するアダプタ。"""

    def render(self, doc):
        raw = document_to_markdown(doc)
        # レンダリング結果を整形して返す
        return mdformat.text(raw)
