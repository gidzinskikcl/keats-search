from data_collection import schemas
from data_collection.segmenters import pdf_segmenter

class PageSegmenter(pdf_segmenter.PdfSegmenter):

    @staticmethod
    def segment(pdf_schema: schemas.PdfSchema) -> list[schemas.PdfSegment]:
        result = []
        for idx, page in enumerate(pdf_schema.pages, start=1):
            result.append(schemas.PdfSegment(parent_file=pdf_schema.file_name, nr=idx, text=page.text))
        return result
