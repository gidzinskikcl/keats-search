from abc import ABC, abstractmethod
from entities import content, document

class Transformer(ABC):
    @abstractmethod
    def transform(self, content: content.Content) -> document.AbstractDocument:
        """
        Transforms input data (e.g. Segment) into output data (e.g. Document).
        """
        pass
