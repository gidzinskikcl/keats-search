import subprocess
import json

from benchmarking.schemas import schemas
from benchmarking.models import search_model

class TFIDFSearchEngine(search_model.SearchModel):
    def __init__(self, jar_path: str, doc_path: str):
        self.jar_path = jar_path
        self.doc_path = doc_path

    def search(self, query: schemas.Query) -> list[schemas.Document]:
        result = subprocess.run(
            [
                "java",
                "-jar", self.jar_path,
                self.doc_path,
                query.question,
                "classic",
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("Java STDERR:", result.stderr)
            raise RuntimeError(f"Lucene search failed: {result.stderr.strip()}")

        ranked = json.loads(result.stdout)
        return [schemas.Document(doc_id=d["documentId"], content=d["content"]) for d in ranked]
