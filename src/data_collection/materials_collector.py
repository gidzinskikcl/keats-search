import pathlib

from data_collection import schemas
from data_collection.extractors import pdf_schema_extractor, transcript_schema_extractor


def collect(
    courses_dir: pathlib.Path, 
    pdf_extractor: pdf_schema_extractor.PdfSchemaExtractor, 
    transcript_extractor: transcript_schema_extractor.TranscriptSchemaExtractor
) -> list[schemas.LectureMaterial]:
    return collect_pdfs(courses_dir, pdf_extractor) + collect_transcripts(courses_dir, transcript_extractor)


def collect_pdfs(courses_dir: pathlib.Path, extractor: pdf_schema_extractor.PdfSchemaExtractor) -> list[schemas.LectureMaterial]:
    pdf_schemas = extractor.extract_all(courses_dir)
    return [
        schemas.LectureMaterial(
            course_name=pdf.course_name,
            title=pdf.file_name,
            content="\n".join(page.text for page in pdf.pages),
            length=len(pdf.pages),
            type=schemas.MaterialType.SLIDES
        )
        for pdf in pdf_schemas
    ]


def collect_transcripts(courses_dir: pathlib.Path, extractor: transcript_schema_extractor.TranscriptSchemaExtractor) -> list[schemas.LectureMaterial]:
    if extractor is None:
        return []   

    transcript_schemas = extractor.extract_all(courses_dir)
    return [
        schemas.LectureMaterial(
            course_name=transcript.course_name,
            title=transcript.file_name,
            content="\n".join(sub.text for sub in transcript.subtitles),
            length=transcript.duration,
            type=schemas.MaterialType.TRANSCRIPT
        )
        for transcript in transcript_schemas
    ]
