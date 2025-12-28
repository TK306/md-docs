"""Covered SPECs: SPEC-RENDER-002 (related: SPEC-RENDER-001)"""

from mddocs.adapters.markdown_adapter import MarkdownRendererAdapter
from mddocs.domain.doc_ir import Document, Paragraph


def test_mdformat_called_once(monkeypatch):
    called = {"count": 0}

    def fake_text(s):
        called["count"] += 1
        return s

    import mddocs.adapters.markdown_renderer as mr

    monkeypatch.setattr(
        mr, "mdformat", type("M", (), {"text": staticmethod(fake_text)})
    )

    adapter = MarkdownRendererAdapter()
    doc = Document(front_matter={}, nodes=[Paragraph("hello")])
    out = adapter.render(doc)
    assert called["count"] == 1
    assert "hello" in out
