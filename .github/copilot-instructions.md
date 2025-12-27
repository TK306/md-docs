# Copilot / AI Agent Instructions for md-docs

This repository has a deliberately small and layered architecture.
Follow these rules strictly — many tests assume these boundaries.

---

## 1. Big picture (non-negotiable)

Purpose:
- Convert Markdown <-> internal Document IR (nodes + front_matter).

Architecture layers:
- src/domain/
  - Pure IR types and serialization logic.
  - Side-effect free. No I/O, no formatting libraries.
- src/interfaces/protocols.py
  - Protocols for dependency injection (Parser / Renderer / Storage).
- src/adapters/
  - Environment-specific implementations.
  - May use external libraries (e.g. mdformat).
- src/usecase/
  - Application logic that wires parser, renderer, and storage.

If you are unsure which layer a change belongs to, STOP and re-evaluate.

---

## 2. Design rules you must not violate

### Dependency Injection
- Usecases must depend on Protocols, not concrete implementations.
- Wiring happens explicitly (see sample_main.py).

### Domain purity
- Domain code MUST NOT import:
  - mdformat
  - pathlib
  - file I/O
- Domain functions return raw data (e.g. unformatted Markdown strings).

### Formatting responsibility
- Domain serializers produce raw Markdown.
- MarkdownRendererAdapter is the ONLY place where mdformat.text() is called.
- Never format the same content twice.

### Front matter handling
- Front matter is parsed from HTML comments:
  <!--
  key: value
  -->
- Stored on Document.front_matter.
- Usecases must pass front_matter to model constructors:
  model_cls.from_nodes(nodes, front_matter)

---

## 3. IR evolution rules (very important)

When modifying or extending the IR (nodes, tables, serializers):

You MUST:
1. Update src/domain/doc_ir.py (types only)
2. Update src/domain/ir_serializers.py
3. Update adapter parser if parsing behavior changes
4. Update tests under tests/spec_tests/

Never:
- Add parsing logic to domain
- Add formatting logic to domain
- Skip serializer updates when adding a new node

IR changes without spec_tests updates are considered incomplete.

---

## 4. Parser philosophy (intentional limitations)

- The Markdown parser is simple and line-oriented by design.
- It intentionally raises MarkdownParseError for malformed input.
- Do NOT silently accept invalid constructs.
- If you extend parsing:
  - Add explicit error cases
  - Update expected exceptions in tests

This is not a full Markdown parser.

---

## 5. Table behavior contract

- Table.as_dict(ignore_extra_columns=False):
  - Raises ValueError if:
    - Row column count != 2
    - Duplicate keys exist
- Do not weaken this behavior silently.
- If changing it, add a new flag or explicit alternative API.

---

## 6. Tests and developer workflow

Python:
- >= 3.11

Tests:
- pytest from project root only
- tests/spec_tests/ define behavioral contracts
- Adapter tests verify integration, not formatting style

Commands:
- pytest -q
- python sample_main.py

---

## 7. Common agent mistakes to avoid

- Do NOT import mdformat outside adapters
- Do NOT bypass Protocols in usecases
- Do NOT extend parser leniency without tests
- Do NOT add logic to domain for convenience

---

## 8. Reference files

- src/domain/doc_ir.py
- src/domain/ir_serializers.py
- src/adapters/markdown_parser.py
- src/adapters/markdown_renderer.py
- src/usecase/convert_usecase.py

If a change touches more than one of these, review all affected layers.

---
