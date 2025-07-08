from fastapi import APIRouter, HTTPException

import config
from core import schemas
from services import bm25_engine

router = APIRouter()
search_engine = bm25_engine.BM25SearchEngine(index_dir=config.settings.INDEX_DIR)


@router.post("/search", response_model=list[schemas.SearchResult])
def search(request: schemas.SearchRequest):
    try:
        results = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            filters=request.filters or schemas.Filter(),
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
