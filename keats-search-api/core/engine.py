from abc import ABC, abstractmethod

from core import schemas


class SearchEngine(ABC):
    @abstractmethod
    def search(
        self, query: schemas.Query, top_k: int, filters: schemas.Filter
    ) -> list[schemas.SearchResult]: ...
