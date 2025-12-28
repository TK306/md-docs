"""Spec-driven tests for public API and contracts.

These tests use SPEC IDs as the test function names to provide a
straightforward mapping between specification items and automated tests.
"""

from pathlib import Path

from mddocs import dump_markdown, DocConvertible
import mddocs.interfaces.protocols as protocols


def test_api_dump_markdown(tmp_path: Path):
    """`dump_markdown` convenience helper should save model to path.

    This verifies the public helper wires default adapters and writes output.
    """

    class SimpleModel(DocConvertible):
        def __init__(self, text: str):
            self.text = text

        def to_nodes(self):
            # Use a simple paragraph node so renderer produces visible text
            from mddocs.domain.doc_ir import Paragraph

            return [Paragraph(self.text)]

        @classmethod
        def from_nodes(cls, nodes, front_matter=None):
            # Not used in this test
            return cls("")

    out = tmp_path / "out.md"
    m = SimpleModel("hello-spec-api")
    dump_markdown(m, out)
    assert out.exists()
    content = out.read_text()
    assert "hello-spec-api" in content


def test_ports_protocols_defined():
    """Protocols for ports must be defined and importable."""

    assert hasattr(protocols, "DocumentParser"), "DocumentParser protocol missing"
    assert hasattr(protocols, "DocumentRenderer"), "DocumentRenderer protocol missing"
    assert hasattr(protocols, "Storage"), "Storage protocol missing"


def test_docconvertible_contract_methods():
    """DocConvertible contract should expose expected methods."""

    assert hasattr(DocConvertible, "to_nodes"), "DocConvertible.to_nodes missing"
    assert hasattr(DocConvertible, "from_nodes"), "DocConvertible.from_nodes missing"
    # to_front_matter is optional but should exist as a callable on the class
    assert hasattr(DocConvertible, "to_front_matter"), (
        "DocConvertible.to_front_matter missing"
    )
