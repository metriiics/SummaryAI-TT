from pydantic import BaseModel
from typing import Union

from fastapi import FastAPI
import uvicorn

from schemas import Documents , Summarization
from pipeline import pipe, pipe_test_pars

app = FastAPI()

class GenerateInput(BaseModel):
    folder_name: str

@app.post("/v1/generate", response_model=Union[Summarization, str])
async def generate(folder: GenerateInput):
    result = await pipe(folder.folder_name)
    return result

@app.post("/v1/test", response_model=Union[list[Documents], str])
def generate_test():
    return pipe_test_pars()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000
    )