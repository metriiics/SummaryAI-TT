from pydantic import BaseModel
from typing import Optional

class ChunkingMetadata(BaseModel):
    length_char: int
    length_word: int
    chunk: int

class ChunkingDocuments(BaseModel):
    content: str
    metadata: ChunkingMetadata

    @classmethod
    def adding(
        cls, 
        text: str, 
        len_char: int, 
        len_word: int, 
        num_chunk: int) -> "ChunkingDocuments":
        
        return cls(
            content=text,
            metadata=ChunkingMetadata(
                length_char=len_char,
                length_word=len_word,
                chunk=num_chunk
            )
        )

class DocMetadata(BaseModel):
    file_type: str
    length_char: int
    length_word: int

class Documents(BaseModel):
    name_docs: str
    content: str
    metadata: DocMetadata

    is_chunked: bool = False
    chunks: Optional[list[ChunkingDocuments]] = None

    def set_chunk(
        self, 
        status: bool, 
        chunks: list[ChunkingDocuments] | None = None
    ) -> "Documents":
        return self.model_copy(
            update={
                "is_chunked": status,
                "chunks": chunks
            }
        )