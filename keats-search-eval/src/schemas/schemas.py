import enum

from dataclasses import dataclass
from typing import Optional

from datetime import timedelta


@dataclass
class PdfPage:
    nr: int
    text: str


@dataclass
class PdfSchema:
    file_name: str
    pages: list[PdfPage]
    url: str
    thumbnail_image: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    lecture_id: Optional[str] = None
    lecture_name: Optional[str] = None


@dataclass
class PdfSegment:
    parent_file: str
    nr: int
    text: str
    url: str
    thumbnail_image: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    lecture_id: Optional[str] = None
    lecture_name: Optional[str] = None


@dataclass
class Timestamp:
    start: timedelta
    end: timedelta


@dataclass
class Subtitle:
    nr: int
    text: str
    timestamp: Timestamp


@dataclass
class Chapter:
    nr: int
    title: str
    timestamp: Timestamp


@dataclass
class TranscriptSchema:
    file_name: str
    duration: timedelta
    subtitles: list[Subtitle]
    url: str
    thumbnail_url: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    lecture_id: Optional[str] = None
    lecture_name: Optional[str] = None
    chapters: Optional[list[Chapter]] = None


@dataclass
class TranscriptSegment:
    nr: int
    parent_file: str
    timestamp: Timestamp
    text: str
    url: str
    thumbnail_url: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    lecture_id: Optional[str] = None
    lecture_name: Optional[str] = None
    chapter_title: Optional[str] = None


class MaterialType(enum.Enum):
    SLIDES = "pdf"
    TRANSCRIPT = "srt"


@dataclass
class LectureMaterial:
    course_name: str
    type: MaterialType
    doc_id: str
    content: str
    length: Optional[int] = (
        None  # for slides: page count; for transcripts: duration in seconds
    )
    lecture_title: str = "N/A"


@dataclass
class DocumentSchema:
    doc_id: str
    content: str
    title: str  # lecture title
    timestamp: Timestamp
    pageNumber: int
    keywords: list[str]
    doc_type: MaterialType
    speaker: str
    course_name: str


@dataclass
class Query:
    id: str
    question: str


@dataclass
class SearchResult:
    document: DocumentSchema
    score: Optional[float] = None
