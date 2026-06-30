from pydantic import BaseModel
from typing import Union

from fastapi import FastAPI
import uvicorn

from schemas import Summarization
from pipeline import pipe

app = FastAPI()

class GenerateInput(BaseModel):
    folder_name: str

@app.post("/v1/generate", response_model=Union[Summarization, str])
async def generate(folder: GenerateInput):
    result = await pipe(folder.folder_name)
    return result

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )