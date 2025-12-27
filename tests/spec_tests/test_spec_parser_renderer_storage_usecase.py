from pathlib import Path

from src.adapters.markdown_adapter import MarkdownParserAdapter, MarkdownRendererAdapter
from src.adapters.markdown_renderer import document_to_markdown
from src.adapters.file_storage import FileStorage
from src.usecase.convert_usecase import ConvertFileUsecase
from src.domain.doc_ir import Paragraph
from src.domain.doc_convertible import DocConvertible


class DummyModel(DocConvertible):
    def __init__(self, text: str):
        self.text = text

    def to_nodes(self):
        return [Paragraph(self.text)]

    @classmethod
    def from_nodes(cls, nodes):
        p = next((n for n in nodes if isinstance(n, Paragraph)), None)
        return cls(p.text if p else "")


def test_SPEC_PARSER_001_and_SPEC_RENDER_001_and_SPEC_STORAGE_001_roundtrip(
    tmp_path: Path,
):
    storage = FileStorage()
    parser_adapter = MarkdownParserAdapter()
    renderer_adapter = MarkdownRendererAdapter()

    # write a simple markdown to a file using storage
    p = tmp_path / "in.md"
    p.write_text("# Title\n\nSome text")

    usecase = ConvertFileUsecase(parser_adapter, renderer_adapter, storage)

    # load model: since no model mapping for this content, use DummyModel via parsing Document nodes
    text = storage.read(p)
    doc = parser_adapter.parse(text)
    # render back with pure renderer (document_to_markdown) to avoid mdformat dependency issues
    out = document_to_markdown(doc)
    assert "# Title" in out

    # test usecase save_model_to_path: create model and save
    m = DummyModel("hello world")
    out_path = tmp_path / "out.md"
    usecase.save_model_to_path(m, out_path)
    # Verify file exists and contains rendered content
    assert out_path.exists()
    content = out_path.read_text()
    assert "hello world" in content
