import pathlib
from typing import List

from data_collection import schemas
from data_collection.extractors import batch_pdf_schema_extractor, batch_transcript_schema_extractor
from data_collection.segmenters import page_segmenter, chapter_segmenter


def collect(
    pdf_courses_dir: pathlib.Path,
    srt_courses_dir: pathlib.Path,
    courses: list[str],
    pdf_extractor: batch_pdf_schema_extractor.BatchPdfSchemaExtractor,
    transcript_extractor: batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor,
    pdf_segmenter: page_segmenter.PageSegmenter,
    srt_segmenter: chapter_segmenter.ChapterSegmenter,
) -> List[schemas.DocumentSchema]:
    pdf_docs = collect_pdf_documents(pdf_courses_dir, courses, pdf_extractor, pdf_segmenter)
    transcript_docs = collect_transcript_documents(srt_courses_dir, courses, transcript_extractor, srt_segmenter)
    return pdf_docs + transcript_docs


def collect_pdf_documents(
    courses_dir: pathlib.Path,
    courses: list[str],
    extractor: batch_pdf_schema_extractor.BatchPdfSchemaExtractor,
    segmenter: page_segmenter.PageSegmenter
) -> List[schemas.DocumentSchema]:
    pdf_schemas = extractor.extract_all(courses_root=courses_dir, courses=courses)

    pdf_segments = []
    for schema in pdf_schemas:
        segments = segmenter.segment(pdf_schema=schema)
        pdf_segments.extend(segments)

    return [
        schemas.DocumentSchema(
            doc_id=f"{seg.parent_file}_{seg.nr}_pdf",
            content=seg.text,
            title=seg.lecture_name or "Untitled",
            timestamp=None,  # No timestamp for slides
            pageNumber=seg.nr,
            keywords=[],
            doc_type=schemas.MaterialType.SLIDES,
            speaker="N/A",
            course_name=seg.course_name,
        )
        for seg in pdf_segments
    ]


def collect_transcript_documents(
    courses_dir: pathlib.Path,
    courses: list[str],
    extractor: batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor,
    segmenter: chapter_segmenter.ChapterSegmenter
) -> List[schemas.DocumentSchema]:
    if extractor is None:
        return []

    transcript_schemas = extractor.extract_all(courses_root=courses_dir, courses=courses)

    transcript_segments = []
    for schema in transcript_schemas:
        segments = segmenter.segment(transcript_schema=schema)
        transcript_segments.extend(segments)

    return [
        schemas.DocumentSchema(
            doc_id=f"{seg.parent_file}_{seg.nr}_srt",
            content=seg.text,
            title=seg.lecture_name or "Untitled",
            timestamp=seg.timestamp,
            pageNumber=seg.nr,
            keywords=[seg.chapter_title] or [],
            doc_type=schemas.MaterialType.TRANSCRIPT,
            speaker="Unknown",
            course_name=seg.course_name,
        )
        for seg in transcript_segments
    ]
