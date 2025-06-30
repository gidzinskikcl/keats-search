from dataclasses import dataclass

from documents import document

@dataclass
class KeatsDocument(document.Document):
    """
    Represents a document (segment) of content from a course, including videos or slides.

    """
    doc_id: str
    parent_file_id: str
    parent_file_name: str
    segment_nr: int
    start_time: str # HH:MM:SS format
    end_time: str   # HH:MM:SS format
    file_type: str
    content_type: str
    length: int
    doc_title: str
    course_ids: list[str]
    course_title: str
    admin_code: str
    speakers: list[str]
    date: str
    source: str
    text: str
    keywords: list[str]
    url: str
    description: str
    notes: str
    version: str