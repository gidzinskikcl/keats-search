from data_collection.transformers import transformer
from entities import segment, document

class Segment2DocumentTransformer(transformer.Transformer):

    def __init__(self):
        """
        This transformer converts a segment into documents based on their metadata.
        """
        self._content = None

    def transform(self) -> document.Document:
        
        if self._content is None:
            raise ValueError("No segments to transform. Please set segments before calling transform().")
        
        file_metadata = self._content.file_metadata
        
        course_id = file_metadata.get("course_id", "unknown_course")
        doc_id = file_metadata.get("doc_id")
        if doc_id is None:
            raise ValueError("Missing required 'doc_id' in segment file_metadata.")


        # Determine file type
        file_extension = file_metadata.get("file_extension", "").lower()
        if file_extension == "pdf":
            file_type = document.FileType.PDF
        elif file_extension == "ppt":
            file_type = document.FileType.PPT
        elif file_extension == "mp4":
            file_type = document.FileType.MP4
        else:
            file_type = document.FileType.UNKNOWN
        content_type = document.ContentType.TEXT 

        # Extract keywords from metadata
        keywords_str = file_metadata.get("keywords", "")
        if isinstance(keywords_str, str):
            keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        else:
            keywords = []

        # Optional fields
        doc_title = file_metadata.get("doc_title", "")
        course_title = file_metadata.get("course_title", "")
        speakers = file_metadata.get("speakers", "")
        date = file_metadata.get("date", "")
        length = int(file_metadata.get("length", "0"))
        url = file_metadata.get("url", "")
        description = file_metadata.get("description", "")
        notes = file_metadata.get("notes", "")
        source = file_metadata.get("source", "")
        version = file_metadata.get("version", "1.0.0")
        is_segmented = file_metadata.get("is_segmented", "True").lower() == "true"

        # Start and end time: for slides, might be empty
        start_time = file_metadata.get("start_time", "")
        end_time = file_metadata.get("end_time", "")

        # Compose Document
        result = document.Document(
            doc_id=doc_id,
            segment_nr=self._content.segment_nr,
            start_time=start_time,
            end_time=end_time,
            file_type=file_type,
            content_type=content_type,
            length=length,
            is_segmented=is_segmented,

            doc_title=doc_title,
            keywords=keywords,
            text=self._content.text,
            url=url,
            course_id=course_id,
            course_title=course_title,
            speakers=speakers,
            date=date,
            description=description,
            notes=notes,
            source=source,
            version=version
        )

        return result
    
    def set_content(self, content: segment.Segment):
        """
        Set the segments to be transformed into a document.
        
        :param segments: A Segment object containing the text and metadata.
        """
        if not isinstance(content, segment.Segment):
            raise TypeError("Expected a Segment object.")
        
        self._content = content

    def get_content(self) -> segment.Segment:
        """
        Get the segments that are set for transformation.
        
        :return: The Segment object containing the text and metadata.
        """
        if self._content is None:
            raise ValueError("No segments have been set. Please set segments before calling get_segment().")
        
        return self._content
