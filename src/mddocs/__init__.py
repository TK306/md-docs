"""Top-level package exports.

This module keeps the public surface small while delegating the implementation
of the convenience API to `mddocs.api`.
"""

from .api import dump_markdown, DocConvertible, nodes

__all__ = ["DocConvertible", "dump_markdown", "nodes"]
