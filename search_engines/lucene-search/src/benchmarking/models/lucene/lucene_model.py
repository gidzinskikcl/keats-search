from benchmarking.models import search_model
from benchmarking.models.lucene import lucene_client
from benchmarking.schemas import schemas


class LuceneModel(search_model.SearchModel):
    def __init__(self, client: lucene_client.LuceneClient):
        self.client = client

    def search(self, query: schemas.Query) -> list[schemas.Document]:
        """
        Converts the incoming query to a raw string and sends it to the LuceneClient.
        Parses the response into Document schema objects.
        """
        raw_query = query.question
        results = self.client.search(raw_query, top_k=10)

        return [
            schemas.Document(
                doc_id=item["documentId"],
                content=item["content"]
            )
            for item in results
        ]
