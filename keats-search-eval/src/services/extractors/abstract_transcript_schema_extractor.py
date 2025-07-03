import pathlib
from abc import ABC, abstractmethod
from schemas import schemas

class AbstractTranscriptSchemaExtractor(ABC):
    @abstractmethod
    def get(self, file_path: pathlib.Path) -> schemas.TranscriptSchema:
        pass