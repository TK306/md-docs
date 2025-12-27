"""src.domain.doc_ir

内部ドキュメント表現（IR: Intermediate Representation）を定義するモジュール。

このモジュールはパース/レンダリングの中間表現として使用されるノード型を提供します。
各ノードはシリアライズとデシリアライズがしやすい単純なデータ構造です。
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class Heading:
    """
    見出しノードを表します。

    Attributes:
        level: 見出しレベル（1 から始まる整数）。
        text: 見出しテキスト。
    """

    level: int
    text: str


@dataclass
class Paragraph:
    """段落ノードを表します。"""

    text: str


@dataclass
class BulletList:
    """箇条書きリスト（unordered list）を表します。"""

    items: list[str]


@dataclass
class NumberedList:
    """番号付きリスト（ordered list）を表します。"""

    items: list[str]


@dataclass
class Table:
    """表を表します。

    Attributes:
        headers: ヘッダ行のセル文字列のリスト。
        rows: 各行ごとのセル文字列のリストのリスト。
    """

    headers: list[str]
    rows: list[list[str]]

    def as_dict(self, ignore_extra_columns: bool = False) -> dict[str, str]:
        """表を辞書に変換して返す。

        - 左列をキー、右列を値として扱う。
        - 各行は少なくとも 2 列必要。2 列より少ない行がある場合は `ValueError` を送出する。
        - 3 列以上の行がある場合はデフォルトで `ValueError` を送出する。`ignore_extra_columns=True`
          を渡すと余分な列を無視して変換する。
        - 同じキーが複数行に現れた場合は `ValueError` を送出する（重複は許可しない）。
        """
        result: dict[str, str] = {}
        for i, row in enumerate(self.rows):
            if len(row) < 2:
                raise ValueError(
                    f"Table.as_dict: row {i} has fewer than 2 columns: {row}"
                )
            if len(row) > 2 and not ignore_extra_columns:
                raise ValueError(
                    f"Table.as_dict: row {i} has more than 2 columns: {row}"
                )
            key = row[0]
            val = row[1]
            if key in result:
                raise ValueError(
                    f"Table.as_dict: duplicate key found: {key!r} at row {i}"
                )
            result[key] = val
        return result


@dataclass
class Image:
    """画像ノードを表します。"""

    alt: str
    path: str


DocNode = Union[
    Heading,
    Paragraph,
    BulletList,
    NumberedList,
    Table,
    Image,
]


@dataclass
class Document:
    """
    ドキュメント全体を表す構造体。

    Attributes:
        front_matter: コメントで表現したフロントマター（キー: 値の辞書）。
        nodes: ドキュメント本文を表す `DocNode` のリスト。
    """

    front_matter: dict[str, str]
    nodes: list[DocNode]
