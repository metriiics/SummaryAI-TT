from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

from schemas import Documents, DocMetadata, ChunkingDocuments, ChunkingMetadata

class Chunked:
    def __init__(self, chunk_size: int, overlap: int = 0, max_size_tokens: int = 5000):
        self.header = [
            ("#", "Header1"),
            ("##", "Header2"),
            ("###", "Header3"),
            ("####", "Header4"),
            ("#####", "Header5"),
            ("######", "Header6")
        ]

        self.max_size_tokens = max_size_tokens
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.splitter_by_text = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.overlap
        )

    def _need_chunking(self, doc: Documents):
        return doc.metadata.predicted_number_tokens >= self.max_size_tokens

    def _smart_splitter_sheme(self, doc: Documents):
        text = doc.content

        for head in self.header:
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[head],
                strip_headers=False
                )
            texts = splitter.split_text(text)
            contents = [text.page_content for text in texts]
            length = [(len(i.split()) * 2.25) for i in contents]
            if max(length) < self.max_size_tokens:
                return head
        return None
    
    def _build_chunks(self, chunks):
        chunk_list: list = []
        for idx, chunk in enumerate(chunks):
            chunk_doc = ChunkingDocuments.adding(
                chunk,
                len(chunk),
                len(chunk.split()),
                idx
            )
            chunk_list.append(chunk_doc)

        return chunk_list

    def _markdown_chunking(self, docs: list[Documents]):
        chunks_docs: list = []

        for doc in docs:
            status_chunking = self._need_chunking(doc)
            
            if not status_chunking:
                doc = doc.set_chunk(status_chunking, None)
                chunks_docs.append(doc)
                continue
            
            chunks = self.splitter_by_text.split_text(doc.content)

            chunk_list = self._build_chunks(chunks)
            
            doc = doc.set_chunk(status_chunking, chunk_list)
            chunks_docs.append(doc)

        return chunks_docs

    def markdown_header_chunking(self, docs: list[Documents]):
        chunks_docs: list = []
        
        for doc in docs:
            status_chunking = self._need_chunking(doc)

            if not status_chunking:
                doc = doc.set_chunk(status_chunking, None)
                chunks_docs.append(doc)
                continue

            head = self._smart_splitter_sheme(doc)
            print(f'Detected heading - {head}')
            if head is None:
                chunks = self.splitter_by_text.split_text(doc.content)

                chunk_list = self._build_chunks(chunks)
                
                doc = doc.set_chunk(status_chunking, chunk_list)
                chunks_docs.append(doc)
            else:
                splitter_by_header = MarkdownHeaderTextSplitter(
                    headers_to_split_on=[head],
                    strip_headers=False
                )
                chunks_struct = splitter_by_header.split_text(doc.content)
                chunks = [chunk.page_content for chunk in chunks_struct]
                
                chunk_list = self._build_chunks(chunks)

                doc = doc.set_chunk(status_chunking, chunk_list)
                chunks_docs.append(doc)
        return chunks_docs