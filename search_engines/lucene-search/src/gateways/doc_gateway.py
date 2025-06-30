from abc import ABC, abstractmethod


class DocumentGateway(ABC):
    """
    Abstract base class for document gateways, defining the common interface for document operations.
    """

    @abstractmethod
    def add(self, documents: list[dict]) -> None:
        """
        Saves a document.

        Args:
            document_data (dict): Data of the document to be saved.
        """
        pass

    @abstractmethod
    def get(self, query: dict) -> list[dict]:
        """
        Retrieves documents based on the provided query.

        Args:
            query (dict): Query to filter documents.
        Returns:
            list[dict]: List of documents matching the query.
        """
        pass

