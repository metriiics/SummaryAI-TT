from fastapi import FastAPI
import uvicorn

from schemas import Documents
from pipeline import pipe

app = FastAPI()

@app.post("/v1/generate", response_model=list[Documents])
def generate():
    return pipe()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )