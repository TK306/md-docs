import pytest

from src.domain.doc_ir import Table
from src.domain.markdown_parser import DocParser
from src.domain.doc_ir import Heading


def test_duplicate_key_raises():
    tbl = Table(headers=["項目", "内容"], rows=[["A", "1"], ["A", "2"]])
    with pytest.raises(ValueError):
        tbl.as_dict()


def test_row_too_few_columns_raises():
    tbl = Table(headers=["項目", "内容"], rows=[["A", "1"], ["B"]])
    with pytest.raises(ValueError):
        tbl.as_dict()


def test_row_too_many_columns_raises_and_ignore_flag():
    tbl = Table(headers=["項目", "内容"], rows=[["A", "1", "x"]])
    with pytest.raises(ValueError):
        tbl.as_dict()

    # ignore_extra_columns=True だと余分な列を無視して成功する
    d = tbl.as_dict(ignore_extra_columns=True)
    assert d == {"A": "1"}


def test_multiple_tables_returned_by_tables():
    t1 = Table(headers=["項目", "内容"], rows=[["k1", "v1"]])
    t2 = Table(headers=["項目", "内容"], rows=[["k2", "v2"]])
    parser = DocParser([Heading(1, "h"), t1, t2])
    tables = parser.tables()
    assert tables == [t1, t2]
