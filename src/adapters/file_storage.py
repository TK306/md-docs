"""src.adapters.file_storage

`Storage` Protocol を満たすファイルベースの実装。
"""

from __future__ import annotations

from pathlib import Path
from src.interfaces.protocols import Storage


class FileStorage(Storage):
    """ファイルに対する簡易的な読み書きアダプタ。"""

    def read(self, path: Path) -> str:
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    def write(self, path: Path, content: str) -> None:
        with path.open("w", encoding="utf-8") as f:
            f.write(content)
