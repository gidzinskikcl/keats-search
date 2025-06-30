import random
from benchmarking.schemas import schemas
from benchmarking.models import search_model


class RandomSearchEngine(search_model.SearchModel):
    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.documents = self._load_documents()

    def _load_documents(self) -> list[schemas.Document]:
        import json
        with open(self.doc_path) as f:
            raw_docs = json.load(f)
        return [schemas.Document(doc_id=doc["documentId"], content=doc["content"]) for doc in raw_docs]

    def search(self, query: schemas.Query) -> list[schemas.Document]:
        return random.sample(self.documents, k=len(self.documents))
