from langgraph.graph import StateGraph, END

from langfuse.langchain import CallbackHandler
from langfuse.types import TraceContext
from langfuse import propagate_attributes

from uuid import UUID

from WorkflowAI.nodes import extract_node, summary_node
from schemas import Documents, State

from dotenv import load_dotenv
load_dotenv()

graph = StateGraph(State)

graph.add_node("Extractor", extract_node)
graph.add_node("Summary", summary_node)

graph.set_entry_point("Extractor")
graph.add_edge("Extractor", "Summary")
graph.add_edge("Summary", END)

GraphApp = graph.compile()

async def ask_ai(docs: list[Documents], trace_id: str, uuid: UUID):
    initial_params = {
        "docs": docs
    }

    langfuse_handler = CallbackHandler(trace_context=
        TraceContext(
            trace_id=trace_id
        )
    )

    with propagate_attributes(
        trace_name=f"Summary-{trace_id}",
        metadata={
            "uuid-query-in-db": uuid
        }
    ):
        result = await GraphApp.ainvoke(
            initial_params,
            config={
                "callbacks": [langfuse_handler]
            }
        )

    return result["summarization"]