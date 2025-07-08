from abc import ABC, abstractmethod
from typing import Union


class TranscriptParser(ABC):
    """
    Abstract base class for parsing video transcripts.
    """

    @abstractmethod
    def get(
        self, subtitle_file: str, load_metadata: bool = True
    ) -> dict[str, Union[str, list[str], list[dict[str, str]]]]:
        pass
