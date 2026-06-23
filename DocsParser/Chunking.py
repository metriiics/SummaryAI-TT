from langchain_text_splitters import MarkdownTextSplitter, MarkdownHeaderTextSplitter

from schemas import Documents, DocMetadata, ChunkingDocuments, ChunkingMetadata

class Chunked:
    def __init__(self, chunk_size, bound):
        self.header = [
            ("#", "Header1"),
            ("##", "Header2")
        ]
        self.bound = bound
        self.chunk_size = chunk_size

        self.splitter_by_header = MarkdownHeaderTextSplitter(headers_to_split_on=self.header)
        self.splitter_by_text = MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=100)

    def _verification(self, doc: Documents):
        return doc.metadata.length_word >= self.bound

    def markdown_chunking(self, docs: list[Documents]):
        chunks_docs: list = []

        for doc in docs:
            status_chunking = self._verification(doc)
            
            if not status_chunking:
                doc = doc.set_chunk(status_chunking, None)
                chunks_docs.append(doc)
                continue
            
            chunks = self.splitter_by_text.split_text(doc.content)

            chunk_list: list = []
            for idx, chunk in enumerate(chunks):
                chunk_doc = ChunkingDocuments.adding(
                    chunk,
                    len(chunk),
                    len(chunk.split()),
                    idx
                )
                chunk_list.append(chunk_doc)
            
            doc = doc.set_chunk(status_chunking, chunk_list)
            chunks_docs.append(doc)

        return chunks_docs

    def markdown_header_chunking(self, doc: Documents):
        chunks = self.splitter_by_header.split_text(doc)
        return chunks
