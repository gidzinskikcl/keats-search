from abc import ABC

class EducationalContentGateway(ABC):
    """
    Abstract base class for all readers.
    Defines the common interface for extracting content from files.
    """

    def get(self) -> dict[str, str]:
        """"""
