from dataclasses import dataclass

@dataclass
class Segment:
    segment_nr: int
    text: str
    file_metadata: dict[str, str]