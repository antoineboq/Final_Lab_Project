import uvicorn
from fastapi import FastAPI
from api import movies, neo4j
import uvicorn


backend = FastAPI(title= "films")

backend.include_router(movies.router)
backend.include_router(neo4j.router)


@backend.get("/")
def root():
    return {"application active"}

if __name__ == "__main__":
    uvicorn.run(backend, host="127.0.0.1", port=8000)


