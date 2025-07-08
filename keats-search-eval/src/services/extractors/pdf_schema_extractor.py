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
        pages = [
            schemas.PdfPage(nr=i, text=page_text)
            for i, page_text in enumerate(parsed_data["text_by_page"], start=1)
        ]

        # Extract optional fields from parsed data
        lecture_id = parsed_data.get("lecture_id")
        lecture_name = parsed_data.get("lecture_title")
        course_id = parsed_data.get("course_id")
        course_name = parsed_data.get("course_title")

        # Create and return the PdfSchema
        return schemas.PdfSchema(
            file_name=file_name,
            pages=pages,
            lecture_id=lecture_id,
            lecture_name=lecture_name,
            course_id=course_id,
            course_name=course_name
        )
