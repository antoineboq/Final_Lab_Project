from fastapi import FastAPI
from api import movies

backend = FastAPI(title= "films")

backend.include_router(movies.router)


@backend.get("/")
def root():
    return {"application active"}

