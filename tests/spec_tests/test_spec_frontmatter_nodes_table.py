"""tests/spec_tests/test_spec_frontmatter_nodes_table.py
Covered SPECs: SPEC-FM-001, SPEC-NODES-001, SPEC-TABLE-001
See: docs/02_外部設計仕様書.md
"""

from src.adapters.markdown_parser import parse_markdown
from src.domain.doc_ir import Table


def test_SPEC_FM_001_front_matter_parsing():
    md = """<!--\ntitle: テスト\n-->\n\n# h\n"""
    doc = parse_markdown(md)
    assert isinstance(doc.front_matter, dict)
    assert doc.front_matter.get("title") == "テスト"


def test_SPEC_NODES_001_node_types():
    md = """
# Heading

Paragraph line.

- item1
- item2

1. one
2. two

| a | b |
| - | - |
| x | y |

![alt](path.png)
"""
    doc = parse_markdown(md)
    types = [type(n).__name__ for n in doc.nodes]
    # Expect at least Heading, Paragraph, BulletList, NumberedList, Table, Image
    assert "Heading" in types
    assert "Paragraph" in types
    assert "BulletList" in types
    assert "NumberedList" in types
    assert "Table" in types
    assert "Image" in types


def test_SPEC_TABLE_001_table_as_dict_rules():
    # valid 2-column table
    t = Table(headers=["k", "v"], rows=[["a", "1"], ["b", "2"]])
    d = t.as_dict()
    assert d == {"a": "1", "b": "2"}

    # row with <2 columns -> ValueError
    t2 = Table(headers=["k"], rows=[["only"]])
    try:
        t2.as_dict()
        assert False, "expected ValueError"
    except ValueError:
        pass

    # row with >2 columns raises by default
    t3 = Table(headers=["k"], rows=[["a", "1", "extra"]])
    try:
        t3.as_dict()
        assert False, "expected ValueError"
    except ValueError:
        pass

    # ignore_extra_columns=True ignores extras
    t4 = Table(headers=["k"], rows=[["a", "1", "extra"]])
    d4 = t4.as_dict(ignore_extra_columns=True)
    assert d4 == {"a": "1"}
