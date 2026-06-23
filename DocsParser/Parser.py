from functools import lru_cache
from docling.document_converter import DocumentConverter
from pathlib import Path

from schemas import Documents, DocMetadata

class ParseDocs:
    def __init__(self):
        self.abs_path = Path.cwd() / "docs"

        self.converter = DocumentConverter()

        self.parsers = {
            ".docx": self.pars_docx_pdf, 
            ".pdf": self.pars_docx_pdf,
            ".xlsx": self.pars_xlsx
        }

    def detect_files(self, name_dir: str) -> list:
        dir = self.abs_path / name_dir
        if not dir.is_dir() or not dir.exists():
            return f"Директория не найдена или не существует: {dir}"

        files = []

        for file in dir.rglob("*"):
            if file.is_file():
                files.append(file)

        return files

    def _clean_txt():
        pass

    def _check_file(self, file: str):
        path = self.abs_path / file
        if path.is_file():
            return path
        else:
            return "Файл не найден или не существует"

    def router(self, files: list):
        parse_content = []

        for file in files:
            if not file.is_file():
                continue

            parser = self.parsers.get(file.suffix.lower())
            if parser is None:
                print(f"Неизвестный формат: {file}")
                continue

            content = parser(file)
            parse_content.append(content)

        return parse_content

    def pars_docx_pdf(self, file: str):
        path = self._check_file(file)

        result = self.converter.convert(path)
        doc = result.document
        markdown = doc.export_to_markdown()
        
        doc = Documents(
            name_docs=path.name,
            content=markdown,
            metadata=DocMetadata(
                file_type=path.suffix,
                length_char=len(markdown),
                length_word=len(markdown.split())
            )
        )

        return doc

    def pars_xlsx(self, file):
        return "XLSX File - Wow!"