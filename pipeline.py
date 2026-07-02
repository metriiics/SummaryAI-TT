from PreProcessingDocs.Chunking import Chunked
from PreProcessingDocs.Parser import ParseDocs

from dbs.queries import Queries

from WorkflowAI.route import ask_ai
from WorkflowAI.observability import predefined_trace_id
from LogConf.log_config import set_logger

from dotenv import load_dotenv
load_dotenv()

logger = set_logger()

parse = ParseDocs()
chunking = Chunked(chunk_size=50_000, max_size_tokens=50_000)
db = Queries()

async def pipe(name_dir: str):
    uid = db.create_summary(proc_id=483675, us_id=234534, trace_id=predefined_trace_id)
    text = parse.router(name_dir)

    if isinstance(text, str):
        return text

    chunks = chunking.markdown_header_chunking(text)
    
    summary = await ask_ai(chunks, predefined_trace_id, uid)
    db.update_summary(
        summary_id=uid, 
        status=True, 
        summary=summary.summary,
        core_info=summary.core_info.model_dump(),
    )
    return summary