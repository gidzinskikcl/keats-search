from abc import ABC, abstractmethod

from documents import document

class DocumentBuilder(ABC):
    @staticmethod
    @abstractmethod
    def build(doc_id: str, data: dict[str, str]) -> document.Document:
        pass
