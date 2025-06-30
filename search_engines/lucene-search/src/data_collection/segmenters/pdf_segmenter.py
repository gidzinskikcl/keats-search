from abc import ABC, abstractmethod

from data_collection import schemas

class PdfSegmenter(ABC):
    @staticmethod
    @abstractmethod
    def segment(pdf_schema: schemas.PdfSchema) -> list[schemas.PdfSegment]:
        """Segments the PDF text into logical sections."""
        pass
