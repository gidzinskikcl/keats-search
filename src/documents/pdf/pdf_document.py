from dataclasses import dataclass

from documents import document
from data_collection.segments import segment

@dataclass
class PDFDocument(document.Document):
    doc_id: str
    file_name: str
    file_extension: str
    course_ids: list[str]
    course_title: str
    admin_code: str
    content_type: str
    page_count: str
    authors: list[str]
    date_created: str
    source: str
    subject: str
    keywords: str
    version: str
    pages: list[segment.Segment]