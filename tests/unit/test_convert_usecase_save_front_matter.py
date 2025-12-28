from pathlib import Path

from mddocs.usecase.convert_usecase import ConvertFileUsecase
from mddocs.domain.doc_convertible import DocConvertible


class DummyStorage:
    def __init__(self):
        self.written = {}

    def read(self, path: Path) -> str:
        return ""

    def write(self, path: Path, content: str) -> None:
        self.written[str(path)] = content


class DummyRenderer:
    def __init__(self):
        self.last_doc = None

    def render(self, doc):
        self.last_doc = doc
        # return something simple
        return "RENDERED"


class ModelWithFrontMatter(DocConvertible):
    def __init__(self, text: str):
        self.text = text

    def to_nodes(self):
        from mddocs.domain.doc_ir import Paragraph

        return [Paragraph(self.text)]

    def to_front_matter(self):
        return {"title": "fm-title"}


def test_save_model_passes_front_matter_to_renderer(tmp_path: Path):
    storage = DummyStorage()
    renderer = DummyRenderer()
    uc = ConvertFileUsecase(parser=None, renderer=renderer, storage=storage)

    m = ModelWithFrontMatter("hello")
    out_path = tmp_path / "out.md"
    uc.save_model_to_path(m, out_path)

    # Renderer should have received a Document with front_matter
    assert renderer.last_doc is not None
    assert renderer.last_doc.front_matter.get("title") == "fm-title"
    # Storage write should have been called
    assert str(out_path) in storage.written
