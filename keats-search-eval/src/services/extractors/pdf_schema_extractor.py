import pathlib

from schemas import schemas
from services.extractors import abstract_pdf_schema_extractor
from services.parsers import pdf_parser

class PdfSchemaExtractor(abstract_pdf_schema_extractor.AbstractPdfSchemaExtractor):
    def __init__(self, parser: pdf_parser.PdfParser):
        self.parser = parser

    def get(self, file_path: pathlib.Path) -> schemas.PdfSchema:
        parsed_data = self.parser.get(file_path=file_path)
        
        # Extract file name from metadata
        file_name = parsed_data["metadata"]["file_name"]

        # Create list of PdfPage objects
        pages = []
        for i, page_text in enumerate(parsed_data["text_by_page"], start=1):
            pages.append(schemas.PdfPage(nr=i, text=page_text))

        # Create and return the PdfSchema
        result =  schemas.PdfSchema(file_name=file_name, pages=pages)
        return result
