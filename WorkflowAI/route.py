from langgraph.graph import StateGraph, END

from WorkflowAI.models import extract_node, summary_node
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

async def ask_ai(docs: list[Documents]):
    initial_params = {
        "docs": docs
    }

    result = await GraphApp.ainvoke(initial_params)

    return result["summarization"]