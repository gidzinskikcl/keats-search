from abc import ABC
from dataclasses import dataclass, asdict
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
class AbstractDocument(ABC):
    """
    Abstract base class for documents, defining common attributes and methods.
    This class is not meant to be instantiated directly.
    """
    doc_id: str

@dataclass
class Document(AbstractDocument):
    """
    Represents a document (segment) of content from a course, including videos or slides.

    Attributes:
        doc_id (str): Unique identifier for the document.
        segment_nr (int): Segment number (e.g., slide number or video segment order).
        start_time (str): Start time of the segment in HH:MM:SS format (for videos).
        end_time (str): End time of the segment in HH:MM:SS format (for videos).
        file_type (FileType): File format (e.g., PDF, PPT, MP4).
        content_type (ContentType): Type of content (e.g., text, video, audio).
        length (int): Duration in seconds (for videos) or number of slides.
        is_segmented (bool): Indicates whether the document is segmented into parts.
        doc_title (str): Title of the document.
        keywords (list[str]): List of topics or keywords relevant to the content.
        text (str): Transcript or extracted text for this segment.
        url (str): Direct link to the video or slides.
        course_id (str): Identifier for the course (e.g., "7CCSMPRJ").
        course_title (str): Title of the course.
        speakers (list[str]): Full names of the professors or speakers.
        date (str): Date of content publication in YYYY-MM-DD format.
        description (str): Description of the video or slides.
        notes (str): Additional notes about the document.
        version (str): Version of the document annotation schema.
        source (str): Origin of the content (e.g., "King’s College" or YouTube channel).
    """
    doc_id: str
    segment_nr: int
    start_time: str # HH:MM:SS format
    end_time: str   # HH:MM:SS format
    file_type: FileType
    content_type: ContentType
    length: int
    is_segmented: bool

    doc_title: str = ""
    keywords: list[str] = None
    text: str = ""
    url: str = ""   
    course_id: str = ""
    course_title: str = ""
    speakers: list[str] = None
    date: str = ""
    description: str = ""
    notes: str = ""
    source: str = ""
    version: str = "1.0.0"

    def to_dict(self) -> dict:
        """
        Converts the Document instance to a dictionary representation.

        Returns:
            dict: Dictionary containing all attributes of the Document.
        """
        doc_dict = asdict(self)
        # Convert Enums to their values
        doc_dict["file_type"] = self.file_type.value
        doc_dict["content_type"] = self.content_type.value
        return doc_dict