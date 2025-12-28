import pytest

from mddocs.adapters.markdown_parser import MarkdownParserImpl, MarkdownParseError


def test_empty_heading_raises():
    md = "#\n"
    p = MarkdownParserImpl()
    with pytest.raises(MarkdownParseError):
        p.parse(md)


def test_invalid_image_syntax_raises():
    md = "![alt](missing"
    p = MarkdownParserImpl()
    with pytest.raises(MarkdownParseError):
        p.parse(md)
