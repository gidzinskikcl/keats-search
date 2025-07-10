import json
import pathlib
from schemas import schemas
from services.extractors import abstract_pdf_schema_extractor
from services.parsers import pdf_parser

URLS = "keats-search-eval/data/slides/urls/urls.json"


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

        # Get url for PDF
        with open(URLS, "r", encoding="utf-8") as f:
            courses = json.load(f)

        url = self._get_url(
            courses=courses,
            course_id=course_id,
            lecture_id=lecture_id,
            file_name=file_name,
        )
        # Get name of thumbnail image file
        thumbnail_image = file_name + "_thumbnail.jpg"

        # Create and return the PdfSchema
        return schemas.PdfSchema(
            file_name=file_name,
            pages=pages,
            lecture_id=lecture_id,
            lecture_name=lecture_name,
            course_id=course_id,
            course_name=course_name,
            url=url,
            thumbnail_image=thumbnail_image,
        )

    def _get_url(
        self,
        courses: dict[str, list[str]],
        course_id: str,
        lecture_id: str,
        file_name: str,
    ) -> str:
        lectures = courses[course_id]

        for idx, url in enumerate(lectures):
            is_lecture = lecture_id in url
            is_file = file_name in url
            if is_file and is_lecture:
                return url
        raise ValueError(f"URL not found for PDF: {file_name}")
