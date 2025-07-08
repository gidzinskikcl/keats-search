from fastapi import APIRouter, HTTPException

from core import schemas
from services import lucene_indexer

router = APIRouter()


@router.post("/index")
def index_documents(request: schemas.IndexRequest):
    try:
        indexer = lucene_indexer.LuceneIndexer(
            index_dir=request.index_dir, json_doc_path=request.document_path
        )
        indexer.index()
        return {"message": "Indexing complete", "index_dir": request.index_dir}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
