from dataclasses import dataclass
from typing import Union


@dataclass
class Heading:
    level: int
    text: str


@dataclass
class Paragraph:
    text: str


@dataclass
class BulletList:
    items: list[str]


@dataclass
class NumberedList:
    items: list[str]


@dataclass
class Table:
    headers: list[str]
    rows: list[list[str]]


@dataclass
class Image:
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
    front_matter: dict[str, str]
    nodes: list[DocNode]
