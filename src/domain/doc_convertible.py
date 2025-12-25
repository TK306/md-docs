from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Type

from src.domain.doc_ir import DocNode
from src.domain.markdown_renderer import document_to_markdown
from src.domain.doc_ir import Document
import mdformat

T = TypeVar("T", bound="DocConvertible")


@dataclass
class DocConvertible(ABC):
    @abstractmethod
    def to_nodes(self) -> list[DocNode]:
        pass

    @classmethod
    @abstractmethod
    def from_nodes(cls: Type[T], nodes: list[DocNode]) -> T:
        pass

    def dump_markdown(self, front_matter: dict[str, str], path: Path) -> None:
        doc = Document(front_matter=front_matter, nodes=self.to_nodes())
        markdown_content = document_to_markdown(doc)

        markdown_content = mdformat.text(markdown_content)

        with path.open("w", encoding="utf-8") as f:
            f.write(markdown_content)

    @classmethod
    def load_markdown(cls: Type[T], path: Path) -> tuple[dict[str, str], T]:
        from src.domain.markdown_parser import parse_markdown

        with path.open("r", encoding="utf-8") as f:
            markdown_content = f.read()

        markdown_content = mdformat.text(markdown_content)

        with path.open("w", encoding="utf-8") as f:
            f.write(markdown_content)

        doc = parse_markdown(markdown_content)
        return doc.front_matter, cls.from_nodes(doc.nodes)
