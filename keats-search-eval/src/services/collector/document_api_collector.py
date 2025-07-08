import pathlib
from typing import List, Optional
from datetime import timedelta
from pydantic import BaseModel, field_serializer
from enum import Enum


from services.extractors import pdf_schema_extractor, transcript_schema_extractor
from services.segmenters import page_segmenter, chapter_segmenter

########################## API ###########################
# Change the schema whenever the api updated


class Timestamp(BaseModel):
    start: timedelta
    end: timedelta

    @field_serializer("start", "end", when_used="always")
    def serialize_time(self, td: Optional[timedelta]) -> Optional[str]:
        if td is None:
            return None
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"


class MaterialType(str, Enum):  # `str` ensures correct JSON serialization
    SLIDES = "pdf"
    TRANSCRIPT = "mp4"


class ApiDocumentSchema(BaseModel):
    id: str  # unique id for this object
    doc_id: str  # id/file name of the paren file
    content: str  # text, speech, content of the lecture segment
    timestamp: Optional[Timestamp] = None  # for transcripts only
    page_number: str  # for pdf (potentially the timestamp number in order)
    lecture_id: str  # id to differentiate between lecture in a corse
    lecture_title: str  # display title
    course_id: str  # e.g 7CCSMPRJ
    course_name: str  # e.g Software Measurement and Testing
    doc_type: MaterialType  # pdf or transcript

    def model_dump_flat(self):
        base = self.model_dump(exclude={"timestamp"})
        if self.timestamp:
            base["start"] = str(self.timestamp.start)
            base["end"] = str(self.timestamp.end)
        return base


########################## API ###########################


def collect_api_documents(
    pdf_courses_dir: pathlib.Path,
    srt_courses_dir: pathlib.Path,
    courses: list[str],
    pdf_extractor: pdf_schema_extractor.PdfSchemaExtractor,
    transcript_extractor: transcript_schema_extractor.TranscriptSchemaExtractor,
    pdf_segmenter: page_segmenter.PageSegmenter,
    srt_segmenter: chapter_segmenter.ChapterSegmenter,
) -> List[ApiDocumentSchema]:
    pdf_docs = collect_pdf_documents_api(
        pdf_courses_dir, courses, pdf_extractor, pdf_segmenter
    )
    transcript_docs = collect_transcript_documents_api(
        srt_courses_dir, courses, transcript_extractor, srt_segmenter
    )
    return pdf_docs + transcript_docs


def collect_pdf_documents_api(
    courses_dir: pathlib.Path,
    courses: list[str],
    extractor: pdf_schema_extractor.PdfSchemaExtractor,
    segmenter: page_segmenter.PageSegmenter,
) -> List[ApiDocumentSchema]:
    pdf_segments = []

    # Loop through all relevant PDF files under matching course folders
    for course_dir in courses_dir.iterdir():
        if course_dir.is_dir() and course_dir.name in courses:
            for lecture_dir in course_dir.iterdir():
                if lecture_dir.is_dir():
                    for pdf_file in lecture_dir.glob("*.pdf"):
                        pdf_schema = extractor.get(pdf_file)
                        segments = segmenter.segment(pdf_schema=pdf_schema)
                        pdf_segments.extend(segments)

    return [
        ApiDocumentSchema(
            id=f"{seg.parent_file}_{seg.nr}_pdf",
            doc_id=seg.parent_file,
            content=seg.text,
            timestamp=None,
            page_number=str(seg.nr),
            lecture_id=seg.lecture_id,
            lecture_title=seg.lecture_name,
            course_id=seg.course_id,
            course_name=seg.course_name,
            doc_type=MaterialType.SLIDES,
        )
        for seg in pdf_segments
    ]


def collect_transcript_documents_api(
    courses_dir: pathlib.Path,
    courses: list[str],
    extractor: transcript_schema_extractor.TranscriptSchemaExtractor,
    segmenter: chapter_segmenter.ChapterSegmenter,
) -> List[ApiDocumentSchema]:
    transcript_segments = []

    for course_dir in courses_dir.iterdir():
        if course_dir.is_dir() and course_dir.name in courses:
            for lecture_dir in course_dir.iterdir():
                if lecture_dir.is_dir():
                    for srt_file in lecture_dir.glob("*.srt"):
                        transcript_schema = extractor.get(srt_file)
                        segments = segmenter.segment(transcript_schema)
                        transcript_segments.extend(segments)

    return [
        ApiDocumentSchema(
            id=f"{seg.parent_file}_{seg.nr}_mp4",
            doc_id=seg.parent_file,
            content=seg.text,
            timestamp=(
                Timestamp(start=seg.timestamp.start, end=seg.timestamp.end)
                if seg.timestamp
                else None
            ),
            page_number=str(seg.nr),
            lecture_id=seg.lecture_id,
            lecture_title=seg.lecture_name,
            course_id=seg.course_id,
            course_name=seg.course_name,
            doc_type=MaterialType.TRANSCRIPT,
        )
        for seg in transcript_segments
    ]
