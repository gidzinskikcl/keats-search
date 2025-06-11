import pathlib
from datetime import timedelta

from data_collection import schemas
from data_collection.extractors import abstract_transcript_schema_extractor
from data_collection.parsers import srt_transcript_parser

class TranscriptSchemaExtractor(abstract_transcript_schema_extractor.AbstractTranscriptSchemaExtractor):
    def __init__(self, parser: srt_transcript_parser.SRTTranscriptParser):
        self.parser = parser

    def get(self, file_path: pathlib.Path) -> schemas.TranscriptSchema:
        parsed_data = self.parser.get(subtitle_file=file_path)

        # Extract file name from metadata
        file_name = parsed_data["file_name"]

        # Create list of Subtitle objects
        subtitles = []
        for i, subtitle in enumerate(parsed_data["transcript"], start=1):
            subtitles.append(schemas.Subtitle(
                nr=i,
                text=subtitle["text"],
                timestamp=schemas.Timestamp(
                    start=self._parse_srt_time(time_str=subtitle["start"]),
                    end=self._parse_srt_time(time_str=subtitle["end"])
                )
            ))

        # Create and return the TranscriptSchema
        result = schemas.TranscriptSchema(
            file_name=file_name,
            duration=timedelta(seconds=int(parsed_data["duration"])),
            subtitles=subtitles
        )
        return result
    
    @staticmethod
    def _parse_srt_time(time_str: str) -> timedelta:
        hours, minutes, seconds_millis = time_str.split(':')
        seconds, millis = seconds_millis.split(',')
        return timedelta(
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(millis)
        )