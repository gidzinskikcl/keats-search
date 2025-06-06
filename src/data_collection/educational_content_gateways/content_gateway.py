from abc import ABC, abstractmethod
from data_structures import segment, content

class EducationalContentGateway(ABC):
    """
    Abstract base class for all readers.
    Defines the common interface for extracting content from files.
    """

    def get(
            self,
            file_path: str,
            metadata: dict[str, str],
    ) -> list[content.Content]:
        """
        Extracts content from the file by applying extraction methods.

        Args:
            file_path (str): Path to the file to be processed.
            metadata (dict[str, str]): Metadata associated with the file.

        Returns:
            list[Content]: List of Content objects with aggregated text and metadata.
        """

    # @abstractmethod
    # def get_text(self, file_path: str, segment_nr: int) -> str:
    #     """
    #     Extract text from the given file and segment.
    #     """
    #     pass

    # @abstractmethod
    # def get_images(self, file_path: str, segment_nr: int) -> List:
    #     """
    #     Extract images from the given file and segment.
    #     """
    #     pass

    # @abstractmethod
    # def get_vector_graphics(self, file_path: str, segment_nr: int) -> List:
    #     """
    #     Extract vector graphics from the given file and segment.
    #     """
    #     pass
