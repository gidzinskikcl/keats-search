from abc import ABC, abstractmethod
from entities import segment, content

class EducationalContentGateway(ABC):
    """
    Abstract base class for all readers.
    Defines the common interface for extracting content from files.
    """

    def get(self) -> list[content.Content]:
        """
        Extracts content from the file by applying extraction methods.

        Args:
            file_path (str): Path to the file to be processed.
            metadata (dict[str, str]): Metadata associated with the file.

        Returns:
            list[Content]: List of Content objects with aggregated text and metadata.
        """
