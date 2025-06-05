from dataclasses import dataclass
import enum

class ContentType(enum.Enum):
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    # IMAGE = "image"
    # VECTOR_GRAPHIC = "vector_graphic"
    UNKNOWN = "unknown"

class FileType(enum.Enum):
    PDF = "pdf"
    PPT = "ppt"
    MP4 = "mp4"
    UNKNOWN = "unknown"

@dataclass
class Document:
    """
    Represents a document (segment) of content from a course, including videos or slides.

    Attributes:
        doc_id (str): Unique identifier for the document.
        doc_title (str): Title of the document.
        segment_nr (int): Segment number (e.g., slide number or video segment order).
        keywords (list[str]): List of topics or keywords relevant to the content.
        text (str): Transcript or extracted text for this segment.
        url (str): Direct link to the video or slides.
        start_time (str): Start time of the segment in HH:MM:SS format (for videos).
        end_time (str): End time of the segment in HH:MM:SS format (for videos).
        course_id (str): Identifier for the course (e.g., "7CCSMPRJ").
        course_title (str): Title of the course.
        speaker (str): Full name of the professor or speaker.
        date (str): Date of content publication in YYYY-MM-DD format.
        file_type (FileType): File format (e.g., PDF, PPT, MP4).
        content_type (ContentType): Type of content (e.g., text, video, audio).
        length (int): Duration in seconds (for videos) or number of slides.
        description (str): Description of the video or slides.
        notes (str): Additional notes about the document.
        is_segmented (bool): Indicates whether the document is segmented into parts.
        version (str): Version of the document annotation schema.
        source (str): Origin of the content (e.g., "King’s College" or YouTube channel).
    """
    doc_id: str
    doc_title: str = ""
    segment_nr: int
    keywords: list[str] = None
    text: str = ""
    url: str = ""   
    start_time: str # HH:MM:SS format
    end_time: str   # HH:MM:SS format
    course_id: str = ""
    course_title: str = ""
    speaker: str = ""
    date: str = ""
    file_type: FileType
    content_type: ContentType
    length: int
    description: str = ""
    notes: str = ""
    is_segmented: bool
    source: str = ""
    version: str = "1.0.0"