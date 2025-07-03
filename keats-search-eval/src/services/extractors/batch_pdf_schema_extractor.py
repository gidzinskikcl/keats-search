import pathlib

from schemas import schemas
from services.extractors import pdf_schema_extractor

class BatchPdfSchemaExtractor:
    def __init__(self, extractor: pdf_schema_extractor.PdfSchemaExtractor):
        self.extractor = extractor

    def extract_all(self, courses_root: pathlib.Path, courses: list[str]) -> list[schemas.PdfSchema]:
        results = []
        for course_dir in courses_root.iterdir():
            if course_dir.is_dir() and course_dir.name in courses:
                course_name = course_dir.name
                for lecture_dir in course_dir.iterdir():
                    if lecture_dir.is_dir():
                        lecture_name = lecture_dir.name
                        for pdf_file in lecture_dir.glob("*.pdf"):
                            pdf_schema = self.extractor.get(pdf_file)
                            pdf_schema.course_name = course_name
                            pdf_schema.lecture_name = lecture_name
                            results.append(pdf_schema)
        return results