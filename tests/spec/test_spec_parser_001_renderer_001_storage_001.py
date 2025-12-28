"""Covered SPECs: SPEC-PARSER-001, SPEC-RENDER-001, SPEC-STORAGE-001"""

from pathlib import Path

from mddocs.adapters.markdown_adapter import (
    MarkdownParserAdapter,
    MarkdownRendererAdapter,
)
from mddocs.adapters.markdown_renderer import document_to_markdown
from mddocs.adapters.file_storage import FileStorage
from mddocs.usecase.convert_usecase import ConvertFileUsecase
from mddocs.domain.doc_ir import Paragraph
from mddocs.domain.doc_convertible import DocConvertible


class DummyModel(DocConvertible):
    def __init__(self, text: str):
        self.text = text

    def to_nodes(self):
        return [Paragraph(self.text)]

    @classmethod
    def from_nodes(cls, nodes):
        p = next((n for n in nodes if isinstance(n, Paragraph)), None)
        return cls(p.text if p else "")


def test_roundtrip(tmp_path: Path):
    storage = FileStorage()
    parser_adapter = MarkdownParserAdapter()
    renderer_adapter = MarkdownRendererAdapter()

    p = tmp_path / "in.md"
    p.write_text("# Title\n\nSome text")

    usecase = ConvertFileUsecase(parser_adapter, renderer_adapter, storage)

    text = storage.read(p)
    doc = parser_adapter.parse(text)
    out = document_to_markdown(doc)
    assert "# Title" in out

    m = DummyModel("hello world")
    out_path = tmp_path / "out.md"
    usecase.save_model_to_path(m, out_path)
    assert out_path.exists()
    content = out_path.read_text()
    assert "hello world" in content
