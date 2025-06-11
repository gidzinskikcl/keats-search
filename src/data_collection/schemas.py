from dataclasses import dataclass
from typing import Optional

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
class LectureMaterial:
    course_name: str
    title: str
    content: str
    page_count: int