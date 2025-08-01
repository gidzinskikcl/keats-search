from schemas import schemas
from services.segmenters import pdf_segmenter


class PageSegmenter(pdf_segmenter.PdfSegmenter):

    @staticmethod
    def segment(pdf_schema: schemas.PdfSchema) -> list[schemas.PdfSegment]:
        result = []
        for idx, page in enumerate(pdf_schema.pages, start=1):
            result.append(
                schemas.PdfSegment(
                    parent_file=pdf_schema.file_name,
                    nr=idx,
                    text=page.text,
                    course_id=pdf_schema.course_id,
                    course_name=pdf_schema.course_name,
                    lecture_id=pdf_schema.lecture_id,
                    lecture_name=pdf_schema.lecture_name,
                    url=pdf_schema.url,
                    thumbnail_image=pdf_schema.thumbnail_image,
                )
            )
        return result
