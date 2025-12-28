"""tests/spec_tests/test_front_matter_propagation.py
Covered SPECs: SPEC-FM-002
See: docs/02_外部設計仕様書.md
"""

from pathlib import Path
from mddocs.usecase.convert_usecase import ConvertFileUsecase
from mddocs.adapters.markdown_parser import MarkdownParserImpl
from mddocs.adapters.markdown_adapter import MarkdownRendererAdapter

from mddocs.interfaces.protocols import Storage
from mddocs.domain.doc_convertible import DocConvertible
from mddocs.domain.doc_cursor import NodeCursor


class DummyStorage(Storage):
    def __init__(self, text: str):
        self._text = text

    def read(self, path: Path) -> str:
        return self._text

    def write(self, path: Path, content: str) -> None:
        raise NotImplementedError()


class DummyModel(DocConvertible):
    """from_cursor を実装して front_matter が渡されることを検証するダミー実装"""

    @classmethod
    def from_cursor(cls, cur: NodeCursor):
        # NodeCursor は front_matter を属性として保持する設計になっている
        fm = getattr(cur, "front_matter", None)
        assert fm is not None, "front_matter が NodeCursor に渡されていません"
        assert fm.get("title") == "test-title"
        return cls()

    def to_nodes(self):
        return []


def test_front_matter_propagation():
    md = """<!--
title: test-title
-->

# Heading
"""
    storage = DummyStorage(md)
    parser = MarkdownParserImpl()
    renderer = MarkdownRendererAdapter()
    uc = ConvertFileUsecase(parser=parser, renderer=renderer, storage=storage)

    # Should not raise and DummyModel.from_cursor will assert the fm
    model = uc.load_model_from_path(Path("dummy.md"), DummyModel)
    assert isinstance(model, DummyModel)
