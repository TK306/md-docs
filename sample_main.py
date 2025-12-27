from pathlib import Path

from src.adapters.file_storage import FileStorage
from src.adapters.markdown_adapter import MarkdownParserAdapter, MarkdownRendererAdapter
from src.usecase.convert_usecase import ConvertFileUsecase


def sample_di_run(path: Path) -> None:
    storage = FileStorage()
    parser = MarkdownParserAdapter()
    renderer = MarkdownRendererAdapter()
    usecase = ConvertFileUsecase(parser, renderer, storage)
    print(usecase)

    # 単純にファイルを読み込み、再レンダリングして出力
    text = storage.read(path)
    doc = parser.parse(text)
    out = renderer.render(doc)
    print(out)


if __name__ == "__main__":
    sample_di_run(Path("input.md"))
