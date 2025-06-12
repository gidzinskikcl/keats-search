import pathlib

from data_collection import schemas
from data_collection.extractors import transcript_schema_extractor


class BatchTranscriptSchemaExtractor:
    def __init__(self, extractor: transcript_schema_extractor.TranscriptSchemaExtractor):
        self.extractor = extractor

    def extract_all(self, courses_root: pathlib.Path) -> list[schemas.TranscriptSchema]:
        results = []
        for course_dir in courses_root.iterdir():
            if course_dir.is_dir():
                course_name = course_dir.name
                for srt_file in course_dir.glob("*.srt"):
                    transcript_schema = self.extractor.get(srt_file)
                    transcript_schema.course_name = course_name
                    results.append(transcript_schema)
        return results