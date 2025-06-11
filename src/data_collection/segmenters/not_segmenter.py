from data_collection import schemas
from data_collection.segmenters import pdf_segmenter

class NotSegmenter(pdf_segmenter.PdfSegmenter):

    @staticmethod
    def segment(pdf_schema: schemas.PdfSchema) -> list[schemas.PdfSegment]:
        # Combine all page texts into one string
        combined_text = "\n".join(page.text for page in pdf_schema.pages)
        
        segment = schemas.PdfSegment(
            parent_file=pdf_schema.file_name,
            nr=1,
            text=combined_text,
        )
        
        result = [segment]
        return result
