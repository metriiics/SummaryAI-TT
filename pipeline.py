from PreProcessingDocs.Chunking import Chunked
from PreProcessingDocs.Parser import ParseDocs

from dbs.queries import Queries

from WorkflowAI.route import ask_ai
from LogConf.log_config import set_logger

logger = set_logger()

parse = ParseDocs()
chunking = Chunked(chunk_size=50_000, max_size_tokens=50_000)
db = Queries()

async def pipe(name_dir: str):
    uid = db.create_summary(483675, 234534)
    text = parse.router(name_dir)

    if isinstance(text, str):
        return text

    chunks = chunking.markdown_header_chunking(text)
    
    summary = await ask_ai(chunks)
    db.update_summary(
        summary_id=uid, 
        status=True, 
        summary=summary.summary,
        core_info=summary.core_info.model_dump(),
        trace_id="12231234"
    )
    return summary