import pathlib

from data_collection import schemas
from data_collection.extractors import pdf_schema_extractor


def collect(courses_dir: pathlib.Path, pdf_extractor: pdf_schema_extractor.PdfSchemaExtractor, transcript_extractor = None) -> list[schemas.LectureMaterial]:
    materials = []

    # Process PDFs
    pdf_schemas = pdf_extractor.extract_all(courses_dir)
    for pdf_schema in pdf_schemas:
        combined_text = "\n".join(page.text for page in pdf_schema.pages)
        page_count = len(pdf_schema.pages)
        materials.append(
            schemas.LectureMaterial(
                course_name=pdf_schema.course_name,
                title=pdf_schema.file_name,
                content=combined_text,
                page_count=page_count
            )
        )

    # Process transcripts
    if transcript_extractor:
        transcript_schemas = transcript_extractor.extract_all(courses_dir)
        for transcript_schema in transcript_schemas:
            combined_text = "\n".join(segment.text for segment in transcript_schema.segments)
            segment_count = len(transcript_schema.segments)
            materials.append(
                schemas.LectureMaterial(
                    course_name=transcript_schema.course_name,
                    title=transcript_schema.file_name,
                    content=combined_text,
                    page_count=segment_count
                )
            )

    return materials
