from datetime import timedelta
from typing import Optional, List
from pydantic import BaseModel, field_serializer
from enum import Enum

import config

class Timestamp(BaseModel):
    start: Optional[timedelta] = None
    end: Optional[timedelta] = None

    @field_serializer("start", "end", when_used="always")
    def serialize_time(self, td: Optional[timedelta]) -> Optional[str]:
        if td is None:
            return None
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

class MaterialType(str, Enum):
    SLIDES = "pdf"
    TRANSCRIPT = "mp4"

class DocumentSchema(BaseModel):
    id: str # unique id for this object
    doc_id: str # id/file name of the paren file 
    content: str # text, speech, content of the lecture segment
    timestamp: Optional[Timestamp] = None# for transcripts only
    page_number: Optional[int] = None # for pdf (potentially the timestamp number in order)
    lecture_id: str # id to differentiate between lecture in a corse
    lecture_title: str # display title
    course_id: str #e.g 7CCSMPRJ
    course_name: str # e.g Software Measurement and Testing
    doc_type: MaterialType # pdf or mp4

class Query(BaseModel):
    question: str

class Filter(BaseModel):
    courses_ids: Optional[List[str]] = None
    lectures_ids: Optional[List[str]] = None
    doc_ids: Optional[List[str]] = None

class SearchResult(BaseModel):
    document: DocumentSchema
    score: Optional[float] = None

class FileEntry(BaseModel):
    doc_id: str
    doc_type: str

class FileInfo(BaseModel):
    lecture: str
    files: list[FileEntry]

class SearchRequest(BaseModel):
    query: Query
    top_k: Optional[int] = config.settings.TOP_K
    filters: Optional[Filter] = None

class IndexRequest(BaseModel):
    document_path: Optional[str] = config.settings.DOC_PATH
    index_dir: Optional[str] = config.settings.INDEX_DIR

class CourseInfo(BaseModel):
    course_id: str
    course_title: str

class LectureInfo(BaseModel):
    lecture_id: str
    lecture_title: str
