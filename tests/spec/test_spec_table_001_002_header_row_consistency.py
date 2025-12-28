"""Covered SPECs: SPEC-TABLE-001, SPEC-TABLE-002"""

from mddocs.domain.doc_ir import Table


def test_header_row_mismatch_allowed():
    t = Table(headers=["a", "b", "c"], rows=[["k1", "v1"], ["k2", "v2"]])
    d = t.as_dict()
    assert d["k1"] == "v1"


def test_row_column_count_enforcement():
    t = Table(headers=["k", "v"], rows=[["only_one"]])
    try:
        t.as_dict()
        assert False, "列数が不足しているのに例外が発生しませんでした"
    except ValueError:
        pass

    t2 = Table(headers=["k", "v"], rows=[["k1", "v1", "extra"]])
    d2 = t2.as_dict(ignore_extra_columns=True)
    assert d2["k1"] == "v1"
