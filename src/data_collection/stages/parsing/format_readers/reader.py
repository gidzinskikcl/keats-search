from abc import ABC, abstractmethod

class Reader(ABC):
    """
    Abstract base class for all readers.
    Defines the common interface for extracting content from files.
    """
    
    @abstractmethod
    def get_text(self, file_path: str) -> str:
        """
        Abstract method to extract text from the given file.
        """
        pass

    @abstractmethod
    def get_images(self, file_path: str) -> list:
        """
        Abstract method to extract images from the given file.
        """
        pass

    @abstractmethod
    def get_vector_graphics(self, file_path: str) -> list:
        """
        Abstract method to extract vector graphics from the given file.
        """
        pass

