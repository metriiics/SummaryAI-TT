from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

from schemas import Documents, Extract, Summarization
from pipeline import pipe, pipe_test_pars
from WorkflowAI.route import ask_ai

app = FastAPI()

class GenerateInput(BaseModel):
    folder_name: str

@app.post("/v1/generate", response_model=Summarization)
async def generate(folder: GenerateInput):
    result = await pipe(folder.folder_name)
    return result

@app.post("/v1/test", response_model=list[Documents])
def generate_test():
    return pipe_test_pars()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )