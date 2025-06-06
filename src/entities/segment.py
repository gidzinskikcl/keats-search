from entities import content

from dataclasses import dataclass

@dataclass
class Segment(content.Content):
    id: str
    text: str
    segment_nr: int
    file_metadata: dict[str, str]