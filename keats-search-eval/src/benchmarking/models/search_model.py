from abc import ABC, abstractmethod

from schemas import schemas


class SearchModel(ABC):
    @abstractmethod
    def search(self, query: schemas.Query) -> list[schemas.SearchResult]:
        """Returns ranked results for a query."""
        pass
