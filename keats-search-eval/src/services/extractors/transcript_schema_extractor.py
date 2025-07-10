import pathlib
from datetime import timedelta

from schemas import schemas
from services.extractors import abstract_transcript_schema_extractor
from services.parsers import srt_transcript_parser


class TranscriptSchemaExtractor(
    abstract_transcript_schema_extractor.AbstractTranscriptSchemaExtractor
):
    def __init__(self, parser: srt_transcript_parser.SRTTranscriptParser):
        self.parser = parser

    def get(self, file_path: pathlib.Path) -> schemas.TranscriptSchema:
        parsed_data = self.parser.get(subtitle_file=file_path)

        # Extract file name from metadata
        file_name = parsed_data["file_name"]

        # Create list of Subtitle objects
        subtitles = []
        for i, subtitle in enumerate(parsed_data["transcript"], start=1):
            subtitles.append(
                schemas.Subtitle(
                    nr=i,
                    text=subtitle["text"],
                    timestamp=schemas.Timestamp(
                        start=self._parse_srt_time(time_str=subtitle["start"]),
                        end=self._parse_srt_time(time_str=subtitle["end"]),
                    ),
                )
            )

        # Chapters
        chapters = []
        for i, chapter in enumerate(parsed_data.get("chapters", []), start=1):
            chapters.append(
                schemas.Chapter(
                    nr=i,
                    title=chapter["title"],
                    timestamp=schemas.Timestamp(
                        start=timedelta(seconds=float(chapter["start_time"])),
                        end=timedelta(seconds=float(chapter["end_time"])),
                    ),
                )
            )

        # Collect additional fields from parsed metadata
        course_id = parsed_data.get("course_id")
        course_name = parsed_data.get("course_title")
        lecture_id = parsed_data.get("lecture_id")
        lecture_name = parsed_data.get("lecture_title")
        url = parsed_data.get("webpage_url")
        thumbnail_url = parsed_data.get("thumbnail")

        # Create and return the TranscriptSchema
        return schemas.TranscriptSchema(
            file_name=file_name,
            duration=timedelta(seconds=int(parsed_data["duration"])),
            subtitles=subtitles,
            chapters=chapters,
            course_id=course_id,
            course_name=course_name,
            lecture_id=lecture_id,
            lecture_name=lecture_name,
            url=url,
            thumbnail_url=thumbnail_url,
        )

    @staticmethod
    def _parse_srt_time(time_str: str) -> timedelta:
        hours, minutes, seconds_millis = time_str.split(":")
        seconds, millis = seconds_millis.split(",")
        return timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(millis),
        )
