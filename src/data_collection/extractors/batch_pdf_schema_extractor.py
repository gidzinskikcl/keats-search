import pathlib

from data_collection import schemas
from data_collection.extractors import pdf_schema_extractor

class BatchPdfSchemaExtractor:
    def __init__(self, extractor: pdf_schema_extractor.PdfSchemaExtractor):
        self.extractor = extractor

    def extract_all(self, courses_root: pathlib.Path) -> list[schemas.PdfSchema]:
        results = []
        for course_dir in courses_root.iterdir():
            if course_dir.is_dir():
                course_name = course_dir.name
                for pdf_file in course_dir.glob("*.pdf"):
                    pdf_schema = self.extractor.get(pdf_file)
                    pdf_schema.course_name = course_name
                    results.append(pdf_schema)
        return results