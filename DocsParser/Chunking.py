from langchain_text_splitters import MarkdownTextSplitter, MarkdownHeaderTextSplitter

from text import text

class Chunked:
    def __init__(self):
        self.header = [
            ("#", "Header1"),
            ("##", "Header2")
        ]

        self.splitter_by_header = MarkdownHeaderTextSplitter(headers_to_split_on=self.header)
        self.splitter_by_text = MarkdownTextSplitter(chunk_size=10000, chunk_overlap=100)

    def MarkdownChunking(self, doc: str):
        chunks = self.splitter_by_text.split_text(doc)
        return chunks

    def MarkdownHeaderChunking(self, doc: str):
        chunks = self.splitter_by_header.split_text(doc)
        return chunks
