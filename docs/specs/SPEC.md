# 概要

本プロジェクトは Markdown 文書を内部表現（IR: DocNode 系）へ変換し、操作（抽出／検索／変換）および Markdown への再レンダリングを行うツール群を提供します。本仕様は開発チームと QA がそのまま実装・受け入れテスト・見積りに使えるレベルの要求（何を満たすべきか）を定義します。設計の詳細は別途設計書で扱います。

## 対象範囲／非対象範囲

- **対象範囲**
  - Markdown テキストを IR（`Document` と `DocNode`）に変換するパース機能（フロントマター、見出し、段落、箇条書き、番号付きリスト、表、画像）。
  - IR から Markdown 文字列へ変換するレンダリング機能（整形・I/O を除く純粋変換）。
  - パース済みノード列の検索・抽出を行うユーティリティ（`DocParser`）。
  - `Table` ノード用の構造化 API（`as_dict`）とそのエラー動作。
  - 上記を検証するユニットテスト群（既存テストを含む）。

- **非対象範囲**
  - ファイル I/O（読み書き）や外部整形ツール呼び出しは本仕様で扱わない（アダプタ／ユースケース層の責務）。
  - GFM の全拡張や高度な Markdown 機能（HTML ブロックの完全な解釈、絵文字等）は本段階では除外。
  - 大規模ドキュメント向けのパフォーマンス最適化は次フェーズとする。

## 機能要件

各要件はユニーク ID、説明、優先度、受け入れ基準（テストで検証可能な具体例）を含む。

- REQ-001: Markdown パーサ（Document と DocNode の生成）
  - 優先度: 高
  - 説明: Markdown を解析して `Document(front_matter: dict[str,str], nodes: list[DocNode])` を生成する。
  - 受け入れ基準:
    - HTML コメント形式のフロントマター（例: `<!--\ntitle: X\n-->`）が存在すれば `Document.front_matter` に正しく格納される。
    - 見出し（`#`）、段落、箇条書き（`- `）、番号リスト（`1. `）、表（`| a | b |`）、画像（`![alt](path)`）が対応する `DocNode` に変換される。
    - 不正な構文は `MarkdownParseError` を投げる。
    - 単体テストで簡単なサンプル Markdown をパースし期待する `Document.nodes` が得られること。

- REQ-002: `DocParser` ユーティリティ
  - 優先度: 高
  - 説明: パース済みノード列から見出し検索、最初の見出し取得、表一覧取得、見出し直後の箇条書き取得を提供する。
  - 受け入れ基準:
    - `find_heading(level:int)` は指定レベルの全 `Heading` を返す。
    - `first_heading(level:int)` は最初の `Heading` または `None` を返す。
    - `tables()` は全 `Table` ノードのリストを返す。
    - `bullet_list_after(heading_text:str, level:int)` は、見出し直後に `BulletList` があればその項目を返す（無ければ空リスト）。

- REQ-003: `Table` ノードと `Table.as_dict`
  - 優先度: 高
  - 説明: 左列をキー、右列を値とする 2 列テーブルを辞書に変換するユーティリティ。列数不整合や重複キーはエラー扱い。
  - 受け入れ基準:
    - `Table.headers: list[str]`, `Table.rows: list[list[str]]` を保持する。
    - `as_dict(ignore_extra_columns: bool=False) -> dict[str,str]` は左列→キー、右列→値の辞書を返す。
    - 行が 2 列未満の場合は `ValueError` を投げる。
    - 行が 3 列以上かつ `ignore_extra_columns==False` の場合は `ValueError`、`ignore_extra_columns==True` の場合は余分列を無視する。
    - 同一キー重複時は `ValueError` を投げる。

- REQ-004: レンダラ（IR → Markdown）
  - 優先度: 中
  - 説明: `Document` / `DocNode` を Markdown 文字列に変換する。出力は整形・I/O を含まない。
  - 受け入れ基準:
    - `render_node(node)` が各ノードを表す Markdown を生成する。
    - `document_to_markdown(doc)` がフロントマターを HTML コメントとして先頭に出力しノード順にレンダリングする。
    - 単体テストで簡単な round-trip（パース→レンダリング→ノード比較）が可能であること。

- REQ-005: 抽象契約 `DocConvertible`
  - 優先度: 低
  - 説明: `to_nodes()` / `from_nodes()` を実装することでドメインオブジェクトが IR と相互変換できることを保証する。
  - 受け入れ基準:
    - サブクラスが `to_nodes()` と `@classmethod from_nodes()` を実装していることをテストで確認できる。

- REQ-006: 例外とエラーの明確化
  - 優先度: 高
  - 説明: パーサ・モデル・ユーティリティの操作で発生する例外を定義する。
  - 受け入れ基準:
    - 不正 Markdown 構文: `MarkdownParseError`
    - `Table.as_dict` の不整合: `ValueError`（行番号・行内容を含むメッセージ推奨）
    - 未対応ノードをレンダラに渡した場合: `TypeError`

## データモデル（主要クラス／構造）

- `Heading`
  - `level: int`（制約: >=1）
  - `text: str`

- `Paragraph`
  - `text: str`

- `BulletList`
  - `items: list[str]`

- `NumberedList`
  - `items: list[str]`

- `Table`
  - `headers: list[str]`
  - `rows: list[list[str]]`（各 `row` は `list[str]`）
  - メソッド: `as_dict(ignore_extra_columns: bool=False) -> dict[str,str]`
  - 制約: `as_dict` 呼び出し時に各行は最低 2 列、重複キーは禁止

- `Image`
  - `alt: str`, `path: str`

- `DocNode` = Union[Heading, Paragraph, BulletList, NumberedList, Table, Image]

- `Document`
  - `front_matter: dict[str,str]`
  - `nodes: list[DocNode]`

## API／インターフェース仕様

- `class DocParser`
  - `__init__(self, nodes: list[DocNode])`
  - `find_heading(self, level: int) -> list[Heading]`
  - `first_heading(self, level: int) -> Heading | None`
  - `tables(self) -> list[Table]`
  - `bullet_list_after(self, heading_text: str, level: int) -> list[str]`
  - 例外: 基本的に例外を発生させないが、入力が期待型でない場合は `TypeError` が発生する可能性がある。

- `class Table`
  - `as_dict(self, ignore_extra_columns: bool=False) -> dict[str,str]`
  - 例外: 列数不整合や重複キーに対して `ValueError` を投げる。

- レンダラ関数
  - `render_node(node: DocNode) -> str` — ノード単位の Markdown 文字列を返す。未対応ノードは `TypeError`。
  - `document_to_markdown(doc: Document) -> str` — フロントマター（コメント形式）＋ノード列を Markdown に変換する。

- `class MarkdownParseError(Exception)` — パース失敗時に送出。

## エラーハンドリング（例外タイプと発生条件）

- `MarkdownParseError`:
  - 発生条件: フロントマター不正、表の不整合、明らかな構文エラー等。

- `ValueError`（`Table.as_dict` 関連）:
  - 発生条件: 行が 2 列未満、3 列以上かつ `ignore_extra_columns==False`、重複キー。
  - 仕様: メッセージに行 index（0 起点）と行内容を含めることを推奨。

- `TypeError`:
  - 発生条件: レンダラが未対応ノードを受け取った場合等。

## ユースケース／シナリオ（入力 → 期待出力）

1. 単純なキー/バリューテーブル（正常系）
   - 入力 Markdown: テーブル（Key/Value）
   - 期待: `Table.rows` が `[ ["name","Alice"], ["age","30"] ]` などとなり、`as_dict()` が `{"name":"Alice","age":"30"}` を返す。

2. 余分な列の扱い（エラー／オプション）
   - 入力: 3 列の行を含むテーブル
   - 期待: `as_dict()` はデフォルトで `ValueError`、`ignore_extra_columns=True` で余分列を無視して変換。

3. 見出し直後の箇条書き抽出
   - 入力: 見出し（`## Features`）の直後に `- A` `- B`
   - 期待: `DocParser(...).bullet_list_after("Features", 2) == ["A","B"]`。

4. フロントマターの読み取り
   - 入力: `<!--\ntitle: Example\nversion: 1.0\n-->` を含むファイル
   - 期待: `Document.front_matter == {"title":"Example","version":"1.0"}`。

5. レンダリングの簡易 round-trip
   - フロー: Markdown をパース → IR を取得 → `document_to_markdown` を実行 → ノード列の等価性で round-trip を確認。

## 受け入れ条件（Definition of Done）とテストマッピング

- Definition of Done:
  - 優先度「高」の要件（REQ-001, REQ-002, REQ-003, REQ-006）が実装され、対応ユニットテストが全てパスしていること。
  - 基本的なレンダラ（REQ-004）の主要ケースが実装され、round-trip が確認できること。
  - `SPEC.md` が `docs/specs/`（またはルート）に追加されレビュー可能な状態であること。

- テストマッピング（既存ファイル）:
  - `tests/test_table_as_dict.py` → REQ-003
  - `tests/test_domain_docparser.py` → REQ-002
  - `tests/test_document_usecases.py` → REQ-001, REQ-004
  - `tests/test_evalitem_errors.py` → REQ-006

## マイルストーン／リリース基準

- M1（最小実装） — リリース条件:
  - REQ-001, REQ-002, REQ-003 の実装完了
  - 対応ユニットテストが CI/ローカルでグリーン
  - `SPEC.md` がレビュー承認されること

- M2（次フェーズ） — 拡張:
  - 高度なレンダリング（複雑表、入れ子リスト等）、パフォーマンス改善、CLI/I/O アダプタ実装

## 補足・運用上の注意

- 例外メッセージはテストで比較される可能性があるため、文言変更はテスト更新を伴うこと。
- `Table.headers` と `rows` の列数不一致はレンダリング/パース双方で注意を要する。必要ならパーサ段階で整合チェックを追加すること。
- API 変更は `SPEC.md` を更新し、該当ユニットテストを追加・修正すること。

---

推奨配置: `docs/specs/SPEC.md`（既にこのファイルを追加しました）。設計書（詳細設計）を作成する場合は、モジュール分割、関数実装の詳細、テストコード例、CI 設定案を次フェーズで提供します。
