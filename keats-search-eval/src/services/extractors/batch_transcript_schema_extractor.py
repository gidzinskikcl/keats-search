import pathlib

from schemas import schemas
from services.extractors import transcript_schema_extractor


class BatchTranscriptSchemaExtractor:
    def __init__(self, extractor: transcript_schema_extractor.TranscriptSchemaExtractor):
        self.extractor = extractor

    def extract_all(self, courses_root: pathlib.Path, courses: list[str]) -> list[schemas.TranscriptSchema]:
        results = []
        for course_dir in courses_root.iterdir():
            if course_dir.is_dir() and course_dir.name in courses:
                course_name = course_dir.name
                for lecture_dir in course_dir.iterdir():
                    if lecture_dir.is_dir():
                        lecture_name = lecture_dir.name
                        for srt_file in lecture_dir.glob("*.srt"):
                            transcript_schema = self.extractor.get(srt_file)
                            transcript_schema.course_name = course_name
                            transcript_schema.lecture_name = lecture_name
                            results.append(transcript_schema)
        return results