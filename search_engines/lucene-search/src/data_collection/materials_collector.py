import pathlib

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
    srt_segmenter: chapter_segmenter.ChapterSegmenter
) -> list[schemas.LectureMaterial]:

    pdfs = collect_pdfs(pdf_courses_dir, courses, pdf_extractor, pdf_segmenter) 
    transcripts = collect_transcripts(srt_courses_dir, courses, transcript_extractor, srt_segmenter)
    return pdfs + transcripts


def collect_pdfs(
        courses_dir: pathlib.Path, 
        courses: list[str],
        extractor: batch_pdf_schema_extractor.BatchPdfSchemaExtractor, 
        segmenter: page_segmenter.PageSegmenter
) -> list[schemas.LectureMaterial]:
    pdf_schemas = extractor.extract_all(courses_root=courses_dir, courses=courses)

    pdf_segments = []
    for s in pdf_schemas:
        seg_schemas = segmenter.segment(pdf_schema=s)
        pdf_segments.extend(seg_schemas)

    return [
        schemas.LectureMaterial(
            course_name=pdf.course_name,
            doc_id=f"{pdf.parent_file}_{pdf.nr}_pdf",
            content=pdf.text,
            type=schemas.MaterialType.SLIDES,
            lecture_title=pdf.lecture_name,
        )
        for pdf in pdf_segments
    ]


def collect_transcripts(
        courses_dir: pathlib.Path, 
        courses: list[str],
        extractor: batch_transcript_schema_extractor.BatchTranscriptSchemaExtractor,
        segmenter: chapter_segmenter.ChapterSegmenter
) -> list[schemas.LectureMaterial]:
    if extractor is None:
        return []
    transcript_schemas = extractor.extract_all(courses_root=courses_dir, courses=courses)

    srt_segments = []
    for t in transcript_schemas:
        segments = segmenter.segment(transcript_schema=t)
        srt_segments.extend(segments)
    
    return [
        schemas.LectureMaterial(
            course_name=segment.course_name,
            doc_id=f"{segment.parent_file}_{segment.nr}_srt",
            content=segment.text,
            type=schemas.MaterialType.TRANSCRIPT,
            lecture_title=segment.lecture_name,
        )
        for segment in srt_segments
    ]
