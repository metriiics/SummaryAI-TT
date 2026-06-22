from pydantic import BaseModel

class DocMetadata(BaseModel):
    file_type: str
    length_char: int
    length_word: int

class Documents(BaseModel):
    name_docs: str
    content: str
    metadata: DocMetadata