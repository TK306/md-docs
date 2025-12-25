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
