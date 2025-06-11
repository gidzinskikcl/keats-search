from abc import ABC, abstractmethod
from typing import Union

class PdfParser(ABC):
    @abstractmethod
    def get(self, file_path: str) -> dict[str, Union[str, list[str]]]:
        """Extracts metadata and text by page from a PDF file."""
        raise NotImplementedError
