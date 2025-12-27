"""Usecase 層: ファイルから Document を読み、モデルへ変換するユースケースの実装例

このモジュールはクリーンアーキテクチャ方針に従い、具体的な I/O 実装には依存せず
`src.interfaces.protocols` の抽象インターフェイスを受け取って動作します。
"""

from __future__ import annotations

from pathlib import Path
from typing import Type

from src.interfaces.protocols import DocumentParser, DocumentRenderer, Storage
from src.domain.doc_convertible import DocConvertible


class ConvertFileUsecase:
    """ファイル → ドメインオブジェクト、ドメインオブジェクト → ファイル を扱うユースケース

    依存性はコンストラクタで注入される: parser, renderer, storage
    """

    def __init__(
        self, parser: DocumentParser, renderer: DocumentRenderer, storage: Storage
    ):
        self.parser = parser
        self.renderer = renderer
        self.storage = storage

    def load_model_from_path(
        self, path: Path, model_cls: Type[DocConvertible]
    ) -> DocConvertible:
        """パスから Markdown を読み込み、指定された `DocConvertible` クラスのインスタンスを返す。

        Raises:
            Exception: パースエラーや変換エラーはそのまま伝搬する（呼び出し側でハンドリング）。
        """
        text = self.storage.read(path)
        doc = self.parser.parse(text)
        return model_cls.from_nodes(doc.nodes)

    def save_model_to_path(self, model: DocConvertible, path: Path) -> None:
        """モデルを Markdown 文字列に変換して指定パスへ保存する。"""
        nodes = model.to_nodes()
        # ラッパー Document を生成してレンダラへ渡す。フロントマターはモデル側で必要に応じ提供される想定
        from src.domain.doc_ir import Document

        doc = Document(front_matter={}, nodes=nodes)
        text = self.renderer.render(doc)
        self.storage.write(path, text)
