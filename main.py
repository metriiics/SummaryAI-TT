from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from schemas import Documents, Extract, Summarization
from pipeline import pipe
from WorkflowAI.route import ask_ai

app = FastAPI()

@app.post("/v1/generate", response_model=Summarization)
def generate():
    return pipe()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )