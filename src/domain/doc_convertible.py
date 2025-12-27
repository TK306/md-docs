"""src.domain.doc_convertible

ドキュメント変換用の抽象基底クラスを定義するモジュール。

設計上の方針:
- 規定クラス（基底クラス）にはフィールドを持たせず、データ保持は派生クラスで行う。
- パース時の自動ファイル上書きは副作用が大きいため、オプションで制御する。
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Callable, cast

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

    def to_front_matter(self) -> dict:
        """
        モデルが提供するフロントマターを返すフック。

        デフォルト実装は空の辞書を返す。具象クラスは必要に応じて
        オーバーライドして `dict[str,str]` を返すこと。

        例: ドメインモデルがメタ情報（title 等）を持つ場合、ここで
        その情報を返すことで `ConvertFileUsecase.save_model_to_path` が
        それをファイルに書き出せる。
        """
        return {}

    @classmethod
    def from_nodes(
        cls: Type[T], nodes: list[DocNode], front_matter: Optional[dict] = None
    ) -> T:
        """
        ノード列からオブジェクトを復元するファクトリメソッドの既定実装。

        具象クラスは次のいずれかを実装できます:
        - `from_nodes(cls, nodes, front_matter=None)` を直接実装する（従来方式）
        - `from_cursor(cls, cur)` を実装して `NodeCursor` を使った実装にする（推奨）

        具象が `from_cursor` を持つ場合は `NodeCursor` を作成して `from_cursor` を呼び出します。
        どちらも実装されていない場合は `NotImplementedError` を送出します。
        """
        # 後方互換: 具象が from_cursor を実装していればそれを用いる
        if hasattr(cls, "from_cursor"):
            from src.domain.doc_cursor import NodeCursor

            cur = NodeCursor(nodes, front_matter or {})
            # 型情報が静的にはないため getattr してキャストしてから呼ぶ
            method = cast(Callable[[NodeCursor], T], getattr(cls, "from_cursor"))
            return method(cur)

        # 既存の具象が from_nodes をオーバーライドしている場合はそちらが使われる
        raise NotImplementedError(
            f"{cls.__name__}.from_nodes is not implemented. Implement either 'from_nodes' or 'from_cursor'."
        )

    # I/O はユースケース / アダプタで扱うため、ここにファイル操作メソッドは置きません。
