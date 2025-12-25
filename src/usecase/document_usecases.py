"""src.usecase.document_usecases

ユースケース（アプリケーション層）のサンプル実装。

このモジュールは、`DocumentParser` / `DocumentRenderer` / `Storage` を引数として受け取り、
ドメインオブジェクト（ここでは `EvalItem`）の読み書きを行います。依存性注入により具体実装
は外から与えられ、テストしやすくなっています。
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from src.interfaces.protocols import DocumentParser, DocumentRenderer, Storage
from src.domain.doc_ir import Document
from src.usecase.eval_item import EvalItem


def load_eval_item(
    path: Path, parser: DocumentParser, storage: Storage
) -> Tuple[dict[str, str], EvalItem]:
    """指定パスから EvalItem を読み込んで返す。

    Args:
        path: 読み込み元のパス。
        parser: `DocumentParser` を実装したオブジェクト。
        storage: `Storage` を実装したオブジェクト。

    Returns:
        (front_matter, EvalItem)
    """
    raw = storage.read(path)
    doc = parser.parse(raw)
    return doc.front_matter, EvalItem.from_nodes(doc.nodes)


def dump_eval_item(
    item: EvalItem,
    front_matter: dict[str, str],
    path: Path,
    renderer: DocumentRenderer,
    storage: Storage,
) -> None:
    """EvalItem を Markdown にレンダリングして指定パスに書き出す。

    Args:
        item: 出力対象の EvalItem。
        front_matter: ドキュメントのフロントマター。
        path: 出力先パス。
        renderer: `DocumentRenderer` を実装したオブジェクト。
        storage: `Storage` を実装したオブジェクト。
    """
    doc = Document(front_matter=front_matter, nodes=item.to_nodes())
    markdown = renderer.render(doc)
    storage.write(path, markdown)
