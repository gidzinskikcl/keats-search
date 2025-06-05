from abc import ABC, abstractmethod

class Transformer(ABC):
    @abstractmethod
    def transform(self, input_data):
        """
        Transforms input data (e.g. Segment) into output data (e.g. Document).
        """
        pass
