from src.domain.markdown_renderer import document_to_markdown
from src.domain.markdown_parser import parse_markdown
from src.domain.doc_ir import Document
from src.usecase.eval_item import EvalItem

item = EvalItem(
    id="E001",
    title="サンプル評価項目",
    eval_type="機能",
    priority="高",
    result="合格",
    conditions=["条件1", "条件2"],
    expected=["期待結果1", "期待結果2"],
)

doc = Document(front_matter={"title": "評価レポート"}, nodes=item.to_nodes())

with open("output.md", "w", encoding="utf-8") as f:
    f.write(document_to_markdown(doc))


with open("input.md", "r", encoding="utf-8") as f:
    markdown_content = f.read()
parsed_doc = parse_markdown(markdown_content)
item = EvalItem.from_nodes(parsed_doc.nodes)

print(item)
