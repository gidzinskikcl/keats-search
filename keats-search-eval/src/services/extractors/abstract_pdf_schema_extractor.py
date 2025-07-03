import pathlib
from abc import ABC, abstractmethod
from schemas import schemas

class AbstractPdfSchemaExtractor(ABC):
    @abstractmethod
    def get(self, file_path: pathlib.Path) -> schemas.PdfSchema:
        """Extracts a PdfSchema from a given PDF file path."""
        pass