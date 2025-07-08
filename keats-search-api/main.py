from fastapi import FastAPI
from routes import search, index, metadata

app = FastAPI(title="Keats Search Service")


@app.get("/")
def root():
    return {"message": "Welcome to Keats Search API"}


@app.get("/status")
def status():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "v1.0", "engine": "bm25"}


app.include_router(search.router)
app.include_router(index.router)
app.include_router(metadata.router)
