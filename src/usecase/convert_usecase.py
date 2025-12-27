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
        # Pass front_matter through to the model factory so implementations
        # that rely on front_matter (or from_cursor) can access it.
        return model_cls.from_nodes(doc.nodes, doc.front_matter)

    def save_model_to_path(self, model: DocConvertible, path: Path) -> None:
        """モデルを Markdown 文字列に変換して指定パスへ保存する。"""
        nodes = model.to_nodes()
        # ラッパー Document を生成してレンダラへ渡す。フロントマターはモデル側で必要に応じ提供される想定
        from src.domain.doc_ir import Document

        # Allow models to optionally provide front_matter. Preferred hooks:
        # - model.to_front_matter() -> dict
        # - model.front_matter attribute
        fm = {}
        if hasattr(model, "to_front_matter") and callable(
            getattr(model, "to_front_matter")
        ):
            try:
                fm = model.to_front_matter()
            except Exception:
                fm = {}
        elif hasattr(model, "front_matter"):
            try:
                fm = getattr(model, "front_matter") or {}
            except Exception:
                fm = {}

        doc = Document(front_matter=fm, nodes=nodes)
        text = self.renderer.render(doc)
        self.storage.write(path, text)
