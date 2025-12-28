# md-docs

## 概要

Markdownと任意構造体を相互変換する

## フォルダ構成

```
.
├── docs: 設計文書
│   ├── 01_要件定義書.md
│   ├── 02_外部設計仕様書.md
│   └── 03_内部設計仕様書.md
├── pyproject.toml
├── README.md
├── src: ソースコード
│   └── mddocs
│       ├── __init__.py
│       ├── adapters
│       │   ├── file_storage.py
│       │   ├── markdown_adapter.py
│       │   ├── markdown_parser.py
│       │   └── markdown_renderer.py
│       ├── domain
│       │   ├── __init__.py
│       │   ├── doc_convertible.py
│       │   ├── doc_cursor.py
│       │   ├── doc_ir.py
│       │   ├── document_inspector.py
│       │   └── ir_serializers.py
│       ├── interfaces
│       │   ├── __init__.py
│       │   └── protocols.py
│       └── usecase
│           ├── __init__.py
│           └── convert_usecase.py
├── tests: テストコード
│   ├── conftest.py
│   ├── spec_tests: 外部設計仕様書と対応するテストコード
│   │   ├── test_front_matter_propagation.py
│   │   ├── test_renderer_mdformat_single_call.py
│   │   ├── test_spec_frontmatter_nodes_table.py
│   │   ├── test_spec_parser_renderer_storage_usecase.py
│   │   └── test_table_header_row_consistency.py
│   └── test_doc_cursor.py
└── uv.lock
```

## 開発環境

* uv
* pre-commit

## Installation

- Install from GitHub (branch or tag):

```
pip install "git+https://github.com/TK306/md-docs.git"
```

- Install from a built wheel (locally):

```
python -m pip install --upgrade build wheel
python -m build
python -m pip install dist/*.whl
```

Note: development tools (mypy, ruff, pytest, pre-commit, import-linter) are listed
under optional dev dependencies and are not installed for normal runtime usage.
