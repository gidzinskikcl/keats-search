from abc import ABC, abstractmethod

from schemas import schemas

class TranscriptSegmenter(ABC):
    @staticmethod
    @abstractmethod
    def segment(transcript_schema: schemas.TranscriptSchema) -> list[schemas.TranscriptSchema]:
        """Segments the .srt Transcript text into sections."""
        pass
