from dataclasses import dataclass

from documents import document
from data_collection.segments import segment

@dataclass
class PPTDocument(document.Document):
    doc_id: str
    file_name: str
    file_extension: str
    doc_title: str
    course_ids: list[str]
    course_title: str
    admin_code: str
    content_type: str
    page_count: str
    authors: list[str]
    created: str
    modified: str
    last_modified_by: str
    source: str
    subject: str
    keywords: str
    comments: str
    revision: str
    category: str
    content_status: str
    identifier: str
    language: str
    version: str
    pages: list[segment.Segment]
