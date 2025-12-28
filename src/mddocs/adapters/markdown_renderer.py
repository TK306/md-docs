"""Adapter renderer: delegate to domain renderer and apply adapter-specific formatting.

The domain owns the pure node->Markdown conversion. The adapter is responsible
for formatting (e.g. `mdformat`) or other environment-specific concerns.
"""

from mddocs.domain.ir_serializers import (
    document_to_markdown as domain_document_to_markdown,
)
from mddocs.domain.doc_ir import Document

# `mdformat` may not be installed in the test environment; expose a
# module-level name that tests can monkeypatch. We will import lazily
# inside the function if not provided.
mdformat = None


def document_to_markdown(doc: Document) -> str:
    raw = domain_document_to_markdown(doc)
    # Adapter-level formatting (keep adapter responsibilities here)
    md = globals().get("mdformat")
    if md is None:
        try:
            import mdformat as _mdformat

            md = _mdformat
        except Exception:
            md = None

    if md is not None and hasattr(md, "text"):
        return md.text(raw)

    return raw
