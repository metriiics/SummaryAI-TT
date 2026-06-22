from pydantic import BaseModel

class DocMetadata(BaseModel):
    file_type: str
    length_char: int
    length_word: int

class Documents(BaseModel):
    name_docs: str
    content: str
    metadata: DocMetadata

class ChunkingMetadata(BaseModel):
    parent_file: str
    length_char: int
    length_word: int
    chunk: int

class ChunkingDocuments(BaseModel):
    name: str
    content: str
    metadata: ChunkingMetadata