"""Adapter renderer: delegate to domain renderer and apply adapter-specific formatting.

The domain owns the pure node->Markdown conversion. The adapter is responsible
for formatting (e.g. `mdformat`) or other environment-specific concerns.
"""

from src.domain.ir_serializers import (
    document_to_markdown as domain_document_to_markdown,
)
from src.domain.doc_ir import Document
import mdformat


def document_to_markdown(doc: Document) -> str:
    raw = domain_document_to_markdown(doc)
    # Adapter-level formatting (keep adapter responsibilities here)
    return mdformat.text(raw)
