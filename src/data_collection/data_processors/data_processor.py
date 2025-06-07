from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """
    Abstract base class for data processors, defining the common interface for processing data.
    """

    @abstractmethod
    def process(self) -> None:
        """
        Processes the data from the specified file path.
        """
        pass