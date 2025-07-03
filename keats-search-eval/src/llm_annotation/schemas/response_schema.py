import enum
from pydantic import BaseModel

class BinaryRelevance(enum.Enum):
    RELEVANT = "relevant"
    NOTRELEVANT = "not relevant"

class AnnotatedPair(BaseModel):
    question: str
    answer: str
    relevance: BinaryRelevance