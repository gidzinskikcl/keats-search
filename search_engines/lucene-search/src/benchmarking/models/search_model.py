from abc import ABC, abstractmethod

from benchmarking.schemas import schemas

class SearchModel(ABC):
    @abstractmethod
    def search(self, query: schemas.Query) -> list[schemas.Document]:
        """Returns ranked results for a query."""
        pass
