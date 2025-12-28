"""tests/spec_tests/test_table_header_row_consistency.py
Covered SPECs: SPEC-TABLE-002, SPEC-TABLE-001
See: docs/02_外部設計仕様書.md
"""

from mddocs.domain.doc_ir import Table


def test_header_row_mismatch_allowed():
    # ヘッダが3列、データ行が2列でも Table インスタンスは作れる（実装上の挙動）
    t = Table(headers=["a", "b", "c"], rows=[["k1", "v1"], ["k2", "v2"]])
    # as_dict は行ごとの列数チェックのみ行うためエラーにならない
    d = t.as_dict()
    assert d["k1"] == "v1"


def test_row_column_count_enforcement():
    # 少なすぎる行はエラー
    t = Table(headers=["k", "v"], rows=[["only_one"]])
    try:
        t.as_dict()
        assert False, "列数が不足しているのに例外が発生しませんでした"
    except ValueError:
        pass

    # 余分な列は ignore_extra_columns=True で許容される
    t2 = Table(headers=["k", "v"], rows=[["k1", "v1", "extra"]])
    d2 = t2.as_dict(ignore_extra_columns=True)
    assert d2["k1"] == "v1"
