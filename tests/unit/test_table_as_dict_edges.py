from mddocs.domain.doc_ir import Table


def test_duplicate_keys_raise_value_error():
    t = Table(headers=["k", "v"], rows=[["a", "1"], ["a", "2"]])
    try:
        t.as_dict()
        assert False, "expected ValueError for duplicate keys"
    except ValueError:
        pass


def test_row_with_too_few_columns_raises():
    t = Table(headers=["k", "v"], rows=[["only_one"]])
    try:
        t.as_dict()
        assert False, "expected ValueError for too few columns"
    except ValueError:
        pass


def test_ignore_extra_columns_allows_overflow():
    t = Table(headers=["k", "v"], rows=[["k1", "v1", "extra"]])
    d = t.as_dict(ignore_extra_columns=True)
    assert d == {"k1": "v1"}
