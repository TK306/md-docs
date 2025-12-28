from mddocs.domain.doc_cursor import NodeCursor
from mddocs.domain.doc_ir import Paragraph, Heading, Table


def test_expect_raises_on_unexpected_type():
    nodes = [Paragraph(text="p1")]
    cur = NodeCursor(nodes)
    try:
        cur.expect(Heading)
        assert False, "expected ValueError when expecting wrong node type"
    except ValueError:
        pass


def test_next_raises_stop_iteration_at_end():
    cur = NodeCursor([])
    try:
        cur.next()
        assert False, "expected StopIteration on empty cursor"
    except StopIteration:
        pass


def test_fork_copies_front_matter_and_position():
    nodes = [Paragraph(text="p1"), Paragraph(text="p2")]
    cur = NodeCursor(nodes, front_matter={"a": "b"})
    _ = cur.next()
    f = cur.fork()
    assert f.front_matter == {"a": "b"}
    assert not f.done
    # fork should start at current position (after one next())
    assert f.peek() is not None


def test_parse_table_as_dict_uses_table():
    t = Table(headers=["k", "v"], rows=[["a", "1"]])
    cur = NodeCursor([t])
    d = cur.parse_table_as_dict()
    assert d == {"a": "1"}
