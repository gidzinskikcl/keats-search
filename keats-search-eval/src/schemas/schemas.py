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
    SLIDES = "SLIDE"
    TRANSCRIPT = "VIDEO_TRANSCRIPT"


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
    id: str  # unique id for this object
    doc_id: str  # id/file name of the paren file
    content: str  # text, speech, content of the lecture segment
    lecture_id: str  # id to differentiate between lecture in a corse
    course_id: str  # e.g 7CCSMPRJ
    doc_type: MaterialType  # pdf or mp4


@dataclass
class Query:
    id: str
    question: str


@dataclass
class SearchResult:
    document: DocumentSchema
    score: Optional[float] = None
