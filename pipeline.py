from DocsParser.Chunking import Chunked
from DocsParser.Parser import ParseDocs

parse = ParseDocs()
chunking = Chunked(chunk_size=10000, bound=1150)

def pipe():
    files = parse.detect_files("RN12390")
    text = parse.router(files)

    chunks = chunking.markdown_chunking(text)
    return chunks
