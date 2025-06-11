import pathlib
from abc import ABC, abstractmethod
from data_collection import schemas

class AbstractTranscriptSchemaExtractor(ABC):
    @abstractmethod
    def get(self, file_path: pathlib.Path) -> schemas.TranscriptSchema:
        pass