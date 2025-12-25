"""テスト実行時の設定

テストディレクトリからプロジェクトルートを sys.path に追加して、
テスト実行中に `src` パッケージをインポート可能にします。
"""

from __future__ import annotations

import sys
from pathlib import Path

# プロジェクトルート (tests/ の親ディレクトリ) を sys.path の先頭に追加
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
