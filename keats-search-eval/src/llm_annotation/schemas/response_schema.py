import enum
from pydantic import BaseModel

from typing import Optional


class BinaryRelevance(enum.Enum):
    RELEVANT = "relevant"
    NOTRELEVANT = "notrelevant"


class AnnotatedPair(BaseModel):
    question: str
    answer: str
    relevance: BinaryRelevance
    # reasoning: Optional[str] = None
