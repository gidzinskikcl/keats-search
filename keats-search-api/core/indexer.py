from abc import ABC, abstractmethod


class DocumentIndexer(ABC):
    @abstractmethod
    def index(self):
        """Index documents into the backend search engine."""
        pass
