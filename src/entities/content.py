from dataclasses import dataclass
from abc import ABC

@dataclass
class Content(ABC):
    id: str
    text: str