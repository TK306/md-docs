from domain.doc_cursor import NodeCursor
from domain.doc_ir import Paragraph, Table, Heading


def test_doccursor_basic_peek_next_expect_collect():
    nodes = [Heading(level=1, text="T"), Paragraph(text="p1"), Paragraph(text="p2")]
    cur = NodeCursor(nodes)

    assert not cur.done
    h = cur.expect(Heading)
    assert h.text == "T"

    # collect paragraph text
    text = cur.collect_paragraph_text()
    assert "p1" in text and "p2" in text
    assert cur.done


def test_parse_table_as_dict():
    table = Table(headers=["k", "v"], rows=[["a", "1"], ["b", "2"]])
    cur = NodeCursor([table])
    d = cur.parse_table_as_dict()
    assert d == {"a": "1", "b": "2"}
