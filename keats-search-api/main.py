import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import search, index, metadata

app = FastAPI(title="Keats Search Service")

thumbnail_dir = os.path.join(os.path.dirname(__file__), "data", "thumbnails")
app.mount("/thumbnails", StaticFiles(directory=thumbnail_dir), name="thumbnails")


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
