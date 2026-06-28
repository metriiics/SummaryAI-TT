from DocsParser.Chunking import Chunked
from DocsParser.Parser import ParseDocs

from WorkflowAI.route import ask_ai

parse = ParseDocs()
chunking = Chunked(chunk_size=50_000, max_size_tokens=50_000)

async def pipe(name_dir: str):
    text = parse.router(name_dir)

    chunks = chunking.markdown_header_chunking(text)
    
    summary = await ask_ai(chunks)
    return summary

def pipe_test_pars():
    text = parse.router("RN12390")

    chunks = chunking.markdown_header_chunking(text)
    return chunks
