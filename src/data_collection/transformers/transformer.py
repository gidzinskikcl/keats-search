from abc import ABC, abstractmethod
from entities import document

class Transformer(ABC):
    @abstractmethod
    def transform(self) -> document.AbstractDocument:
        """
        Transforms input data (e.g. Segment) into output data (e.g. Document).
        """
        pass

    @abstractmethod
    def set_content(self, content: document.AbstractDocument) -> None:
        """
        Sets the content to be transformed.
        
        Args:
            content (document.AbstractDocument): The content to be transformed.
        """
        pass

    @abstractmethod
    def get_content(self) -> document.AbstractDocument:
        """
        Gets the content that is set for transformation.
        
        Returns:
            document.AbstractDocument: The content to be transformed.
        """
        pass
