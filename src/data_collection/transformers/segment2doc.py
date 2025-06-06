from data_collection.transformers import transformer
from data_structures.segment import Segment
from data_structures.document import Document, FileType, ContentType

class Segment2DocumentTransformer(transformer.Transformer):
    def transform(self, segment: Segment) -> Document:
        file_metadata = segment.file_metadata
        
        # Derive doc_id using a combination of course_id, segment number, or other logic
        course_id = file_metadata.get("course_id", "unknown_course")
        # get doc_id from segment file metadata
        doc_id = file_metadata.get("doc_id")
        if doc_id is None:
            raise ValueError("Missing required 'doc_id' in segment file_metadata.")


        # Determine file type (basic example)
        file_extension = file_metadata.get("file_extension", "").lower()
        if file_extension == "pdf":
            file_type = FileType.PDF
        elif file_extension == "ppt":
            file_type = FileType.PPT
        elif file_extension == "mp4":
            file_type = FileType.MP4
        else:
            file_type = FileType.UNKNOWN

        # Determine content type
        content_type = ContentType.TEXT  # Defaulting to text here

        # Extract keywords from metadata
        keywords_str = file_metadata.get("keywords", "")
        if isinstance(keywords_str, str):
            keywords = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        else:
            keywords = []

        # Optional fields
        doc_title = file_metadata.get("doc_title", "")
        course_title = file_metadata.get("course_title", "")
        speaker = file_metadata.get("speaker", "")
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
        document = Document(
            doc_id=doc_id,
            segment_nr=segment.segment_nr,
            start_time=start_time,
            end_time=end_time,
            file_type=file_type,
            content_type=content_type,
            length=length,
            is_segmented=is_segmented,

            doc_title=doc_title,
            keywords=keywords,  # Could be extracted later
            text=segment.text,
            url=url,
            course_id=course_id,
            course_title=course_title,
            speaker=speaker,
            date=date,
            description=description,
            notes=notes,
            source=source,
            version=version
        )

        return document
