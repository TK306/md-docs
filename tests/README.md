テスト配置と命名規則

目的:
- `tests/spec/` : 外部設計（SPEC-...）に対する回帰テスト。ユーザや他システムから見た振る舞いを検証します。
- `tests/unit/` : 内部実装の詳細、境界条件、ヘルパ関数の単体テスト。

ルール:
- `tests/spec/` のテストは可能な限り公開 API（`mddocs` のトップレベルや adapters を通した API）を使って検証すること。
- `tests/unit/` は内部モジュール（`mddocs.domain` 等）を直接インポートして細かい単体検証を行うこと。
- ファイル名:
  - spec: `test_spec_<spec-id>_<short-desc>.py`（例: `test_spec_fm_002_front_matter_propagation.py`）
  - unit: `test_<module>_<case>.py`（例: `test_table_as_dict_edges.py`）
- 各 spec ファイルの先頭に `Covered SPECs: ...` コメントを記載し、どの外部設計の項目を検証しているか明示すること。

CI 実行順（推奨）:
1. `tests/spec/` を実行して外部仕様の回帰を確認
2. `tests/unit/` を実行して内部の回帰を確認

移行時注意:
- 既存テストがどちらに属するか判断が難しい場合は、まず `tests/spec/` に置き外部からの振る舞いを確認し、内部の境界条件に踏み込む検査は `tests/unit/` に移す。

問い合わせ:
- ルールの適用に迷ったら `README.md` を更新して明記します。