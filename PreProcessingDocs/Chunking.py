from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from typing import Optional

from schemas import Documents, ChunkingDocuments

class Chunked:
    """ 
        Класс реализует алгоритм чанкирования больших документов.

        Реализует две стратегии разбиения:
            1. Рекурсивное разбиение по тексту (RecursiveCharacterTextSplitter)
            2. Разбиение по заголовкам Markdown (MarkdownHeaderTextSplitter)

        Автоматическое определение чанкирования на основе максимального количества токенов(max_size_tokens)
        Автоматический выбор подходящего уровня заголовка для оптимального деления без потери смысла 
        Стратегия необходимости чанкирования реализуется:
            - Если найден оптимальный заголовок Markdown производится чанкирование на основе заголовка
            - Иначе производится рекурсивное чанкирование
                
    """
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

    def _need_chunking(self, doc: Documents) -> bool:
        """ Проверка необходимости чанкирования документа """
        return doc.metadata.predicted_number_tokens >= self.max_size_tokens

    def _smart_splitter_sheme(self, doc: Documents) -> Optional[tuple[str, str]]:
        """ Определяет оптимальный уровень заголовков(H1 - H6) для разбиения документа. """
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
    
    def _build_chunks(self, chunks) -> list[ChunkingDocuments]:
        """ Создание структурированных объектов чанков из списка текстовых фрагментов """
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

    def markdown_header_chunking(self, docs: list[Documents]) -> list[Documents]:
        """ 
            Основной метод для "умного" разбиения документов с учетом заголовков.
        
            Реализует стратегию:
                1. Если документ не превышает лимит - оставляет без изменений
                2. Если превышает - пытается найти оптимальный уровень заголовков
                3. При успешном поиске - разбивает по заголовкам
                4. При неудаче - использует рекурсивное разбиение по тексту
        """
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