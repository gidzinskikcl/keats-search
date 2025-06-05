from abc import ABC, abstractmethod

class Parser(ABC):
    """
    Abstract base class for all parsers.
    Defines the common interface for parsing files.
    """
    
    @abstractmethod
    def parse_text(self, file_path: str) -> str:
        """
        Abstract method to parse text from the given file.
        """
        pass

    @abstractmethod
    def parse_images(self, file_path: str) -> list:
        """
        Abstract method to parse images from the given file.
        """
        pass

    @abstractmethod
    def parse_vector_graphics(self, file_path: str) -> list:
        """
        Abstract method to parse vector graphics from the given file.
        """
        pass

