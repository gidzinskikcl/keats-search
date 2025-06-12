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
    course_name: Optional[str] = None

@dataclass
class PdfSegment:
    parent_file: str
    nr: int
    text: str

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
class TranscriptSchema:
    file_name: str
    duration: timedelta
    subtitles: list[Subtitle]
    course_name: Optional[str] = None

@dataclass
class TranscriptSegment:
    parent_file: str
    timestamp: Timestamp
    text: str

@dataclass
class Chapter:
    nr: int
    title: str
    timestamp: Timestamp

class MaterialType(enum.Enum):
    SLIDES = "slides"
    TRANSCRIPT = "transcript"

@dataclass
class LectureMaterial:
    course_name: str
    type: MaterialType
    title: str
    content: str
    length: int # for slides: page count; for transcripts: duration in seconds