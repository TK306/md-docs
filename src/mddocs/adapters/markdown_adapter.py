"""src.adapters.markdown_adapter

`DocumentParser` / `DocumentRenderer` の具体実装ラッパー。
内部で既存の `parse_markdown` / `document_to_markdown` を呼び出し、必要に応じて
追加の整形（`mdformat`）を行います。
"""

from __future__ import annotations

from mddocs.interfaces.protocols import DocumentParser, DocumentRenderer
from mddocs.adapters.markdown_renderer import document_to_markdown
from mddocs.adapters.markdown_parser import MarkdownParserImpl


class MarkdownParserAdapter:
    """Adapter that delegates to a `DocumentParser` implementation.

    Default parser is `MarkdownParserImpl`, but a different implementation
    (e.g. a mock) can be injected for testing or alternate behavior.
    """

    def __init__(self, parser: DocumentParser | None = None):
        self._parser = parser or MarkdownParserImpl()

    def parse(self, text: str):
        return self._parser.parse(text)


class MarkdownRendererAdapter(DocumentRenderer):
    """`document_to_markdown` をラップし、出力時に `mdformat` で整形するアダプタ。"""

    def render(self, doc):
        # `document_to_markdown` from the renderer already returns formatted
        # Markdown (adapter-level). Avoid double-formatting here.
        return document_to_markdown(doc)
