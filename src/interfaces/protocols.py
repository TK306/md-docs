"""src.interfaces.protocols

ドメインとインフラストラクチャの間で利用する Protocol（抽象インターフェース）を定義します。

これらの Protocol を使ってユースケースは具体実装に依存せずに振る舞いを記述でき、テスト時にはモック
を注入して容易に単体テストできます。
"""

from __future__ import annotations

from typing import Protocol
from pathlib import Path

from src.domain.doc_ir import Document


class DocumentParser(Protocol):
    """文字列（Markdown）から `Document` を生成する責務を表すプロトコル。"""

    def parse(self, text: str) -> Document: ...


class DocumentRenderer(Protocol):
    """`Document` を文字列（Markdown）に変換する責務を表すプロトコル。"""

    def render(self, doc: Document) -> str: ...


class Storage(Protocol):
    """外部ストレージ（ファイル等）の読み書きを抽象化するプロトコル。"""

    def read(self, path: Path) -> str: ...

    def write(self, path: Path, content: str) -> None: ...
