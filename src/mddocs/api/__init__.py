"""Public convenience API for simple scripting usage.

Place helpers here so consumers can `from mddocs import dump_markdown` while
keeping the implementation separated under `mddocs.api`.
"""

from __future__ import annotations

from pathlib import Path

from ..domain.doc_convertible import DocConvertible
from ..usecase.convert_usecase import ConvertFileUsecase
from ..adapters.file_storage import FileStorage
from ..adapters.markdown_adapter import (
    MarkdownParserAdapter,
    MarkdownRendererAdapter,
)

# Expose the nodes namespace for convenience (now kept inside the api package)
from . import nodes  # noqa: F401


def dump_markdown(model: DocConvertible, path: str | Path) -> None:
    """Save a `DocConvertible` to `path` using default adapters.

    This is intentionally minimal — it wires default parser/renderer/storage
    and calls the usecase. Suitable for examples and simple scripts.
    """
    uc = ConvertFileUsecase(
        parser=MarkdownParserAdapter(),
        renderer=MarkdownRendererAdapter(),
        storage=FileStorage(),
    )
    uc.save_model_to_path(model, Path(path))


__all__ = ["DocConvertible", "dump_markdown", "nodes"]
