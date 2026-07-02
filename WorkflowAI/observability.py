from langfuse import Langfuse

from schemas import ScoresTracing

import os
from dotenv import load_dotenv
load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL")
) 

predefined_trace_id = langfuse.create_trace_id()

async def create_score_tracing(score: ScoresTracing):
    langfuse.create_score(
        trace_id=score.trace_id,
        name="user-feedback",
        value=score.value,
        data_type="NUMERIC",
        comment=score.comment
    )

    langfuse.flush()