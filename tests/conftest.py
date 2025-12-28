"""pytest fixtures for tests.

共通で使われるパーサ／レンダラ／ストレージのインスタンスを提供します。
これにより各テストファイルでの重複インスタンス化を減らします。
"""

from __future__ import annotations

import pytest

from mddocs.adapters.markdown_parser import MarkdownParserImpl
from mddocs.adapters.markdown_adapter import (
    MarkdownParserAdapter,
    MarkdownRendererAdapter,
)
from mddocs.adapters.file_storage import FileStorage


@pytest.fixture
def parser_impl() -> MarkdownParserImpl:
    return MarkdownParserImpl()


@pytest.fixture
def parser_adapter() -> MarkdownParserAdapter:
    return MarkdownParserAdapter()


@pytest.fixture
def renderer_adapter() -> MarkdownRendererAdapter:
    return MarkdownRendererAdapter()


@pytest.fixture
def file_storage() -> FileStorage:
    return FileStorage()


@pytest.fixture
def parse_text(parser_impl):
    """Helper fixture: parse plain markdown text to Document using parser_impl."""

    def _parse(text: str):
        # MarkdownParserImpl は parse(text) メソッドを持つ想定
        return parser_impl.parse(text)

    return _parse
