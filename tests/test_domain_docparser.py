from src.domain.markdown_parser import DocParser
from src.domain.doc_ir import Heading, Table, BulletList, Paragraph


# DocParser のユニットテスト群
# 目的: ノード列を操作するユーティリティが期待どおりに見出し/表/箇条書きを検索・抽出できることを検証
def test_find_and_first_heading():
    # 見出し検索の成功ケースと存在しない場合の None を確認
    nodes = [
        Heading(2, "Intro"),
        Heading(3, "E001 タイトル"),
        Paragraph("some text"),
        Heading(3, "E002 別タイトル"),
    ]

    parser = DocParser(nodes)

    # find_heading: 指定レベルの見出しが全て返る
    h3 = parser.find_heading(3)
    assert len(h3) == 2
    assert h3[0].text == "E001 タイトル"

    # first_heading: 最初の見出しが返る
    first = parser.first_heading(3)
    assert first is not None
    assert first.text == "E001 タイトル"

    # 存在しないレベルは None
    assert parser.first_heading(5) is None


def test_table_as_dict_and_missing_table():
    # tables() がドキュメント中の Table ノードを list[Table] で返すことを検証
    tbl = Table(headers=["項目", "内容"], rows=[["種別", "機能"], ["優先度", "高"]])
    nodes = [Heading(3, "H"), tbl]
    parser = DocParser(nodes)
    tables = parser.tables()
    # 1 つの Table が返る
    assert len(tables) == 1
    assert tables[0] is tbl
    # 行データが正しいことを確認（左列/右列）
    rows = tables[0].rows
    assert [rows[0][0], rows[0][1]] == ["種別", "機能"]

    # 表がない場合は空リストを返す
    parser2 = DocParser([Heading(1, "h")])
    assert parser2.tables() == []


def test_bullet_list_after():
    # heading の直後にある BulletList を取得できることを検証
    bl = BulletList(["c1", "c2"])
    nodes = [Heading(4, "条件"), bl]
    parser = DocParser(nodes)

    res = parser.bullet_list_after("条件", level=4)
    assert res == ["c1", "c2"]

    # 存在しない見出しの後は空リスト
    assert parser.bullet_list_after("期待結果", level=4) == []
