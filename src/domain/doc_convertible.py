"""src.domain.doc_convertible

ドキュメント変換用の抽象基底クラスを定義するモジュール。

設計上の方針:
- 規定クラス（基底クラス）にはフィールドを持たせず、データ保持は派生クラスで行う。
- パース時の自動ファイル上書きは副作用が大きいため、オプションで制御する。
"""

from pathlib import Path
from abc import ABC, abstractmethod
from typing import TypeVar, Type

from src.domain.doc_ir import DocNode
from src.domain.markdown_renderer import document_to_markdown
from src.domain.doc_ir import Document
import mdformat

# 基底クラスをバインドしておくことで Type[T] が from_nodes を持つことを静的に示す
T = TypeVar("T", bound="DocConvertible")


class DocConvertible(ABC):
    """
    ドキュメント（Markdown 等）と相互変換できるオブジェクトの抽象基底クラス。

    サブクラスはデータ保持のために `@dataclass` を利用することを想定します。
    基底クラス自身はフィールドを持たないため、`@dataclass` は付けていません。
    """

    @abstractmethod
    def to_nodes(self) -> list[DocNode]:
        """
        オブジェクトを内部ドキュメント表現（`DocNode` のリスト）に変換します。

        Returns:
            list[DocNode]: ドキュメントレンダラへ渡すノード列。
        """
        pass

    @classmethod
    @abstractmethod
    def from_nodes(cls: Type[T], nodes: list[DocNode]) -> T:
        """
        ノード列からオブジェクトを復元するファクトリメソッド。

        Args:
            nodes: パース済みのドキュメントノード列。

        Returns:
            T: サブクラスのインスタンス。
        """
        pass

    def dump_markdown(self, front_matter: dict[str, str], path: Path) -> None:
        """
        オブジェクトを Markdown にレンダリングしてファイルに書き出します。

        Args:
            front_matter: ドキュメントのフロントマター（タイトルや日付など）。
            path: 出力先ファイルパス。

        Note:
            出力時に `mdformat` で整形を行い、整形済みの文字列を書き込みます。
        """
        doc = Document(front_matter=front_matter, nodes=self.to_nodes())
        markdown_content = document_to_markdown(doc)

        markdown_content = mdformat.text(markdown_content)

        with path.open("w", encoding="utf-8") as f:
            f.write(markdown_content)

    @classmethod
    def load_markdown(
        cls: Type[T], path: Path, format_on_load: bool = False
    ) -> tuple[dict[str, str], T]:
        """
        Markdown ファイルを読み込み、パースしてオブジェクトを復元します。

        Args:
            path: 読み込み元の Markdown ファイルパス。
            format_on_load: True の場合、`mdformat` で整形した結果を同じファイルに上書きします。
                            デフォルトは False（副作用なし）。

        Returns:
            (front_matter, instance): フロントマターと復元されたサブクラスのインスタンス。
        """
        from src.domain.markdown_parser import parse_markdown

        with path.open("r", encoding="utf-8") as f:
            markdown_content = f.read()

        formatted = mdformat.text(markdown_content)

        if format_on_load and formatted != markdown_content:
            with path.open("w", encoding="utf-8") as f:
                f.write(formatted)

        doc = parse_markdown(formatted)
        return doc.front_matter, cls.from_nodes(doc.nodes)
