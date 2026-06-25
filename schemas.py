from pydantic import BaseModel, Field
from typing import Optional

class ChunkingMetadata(BaseModel):
    length_char: int
    length_word: int
    predicted_number_tokens: float
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
                predicted_number_tokens=len_word * 2.25,
                chunk=num_chunk
            )
        )

class DocMetadata(BaseModel):
    file_type: str
    length_char: int
    length_word: int
    predicted_number_tokens: float

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
    
class Extract(BaseModel):
    main_info: str = Field(description="")
    resource: list[str] | str = Field(description="")

class ExtractorInput(BaseModel):
    content: str

class Summarization(BaseModel):
    detailed_content: str = Field(description="Подробное саммари")
    short_content: str = Field(description="Краткая саммари")
    resource: list[str] = Field(description="Источники")

class State(BaseModel):
    docs: list[Documents] 
    extracts: Optional[list[Extract]] = None
    summarization: Optional[Summarization] = None