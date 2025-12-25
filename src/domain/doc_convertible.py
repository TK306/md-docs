"""src.domain.doc_convertible

ドキュメント変換用の抽象基底クラスを定義するモジュール。

設計上の方針:
- 規定クラス（基底クラス）にはフィールドを持たせず、データ保持は派生クラスで行う。
- パース時の自動ファイル上書きは副作用が大きいため、オプションで制御する。
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Type

from src.domain.doc_ir import DocNode

# 基底クラスをバインドしておくことで Type[T] が from_nodes を持つことを静的に示す
T = TypeVar("T", bound="DocConvertible")


class DocConvertible(ABC):
    """
    ドキュメント変換可能なオブジェクトの抽象基底クラス（副作用なし）。

    注意:
        - I/O（ファイルの読み書き）や文字列整形（`mdformat`）はこのクラスの責務ではありません。
        - 文字列との相互変換やファイル入出力はユースケース / アダプタを通じて行ってください。
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

    # I/O はユースケース / アダプタで扱うため、ここにファイル操作メソッドは置きません。
