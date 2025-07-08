import enum

from pydantic import BaseModel


class DifficultyLevel(enum.Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Query(BaseModel):
    question: str
    label: DifficultyLevel
    answer: str


class QuerySet(BaseModel):
    questions: list[Query]
