from dataclasses import dataclass

from typing import Iterator, OrderedDict, Optional

import enum

@dataclass
class Document:
    doc_id: str
    content: str
    course: str
    lecture: str
    score: Optional[float] = None

@dataclass
class Query:
    id: str
    question: str

class RelevanceScore(enum.Enum):
    IRRELEVANT = 0
    SLIGHTLY_RELEVANT = 1
    MODERATELY_RELEVANT = 2
    HIGHLY_RELEVANT = 3

class Relevance(enum.Enum):
    RELEVANT = "RELEVANT"
    NOTRELEVANT = "NOT RELEVANT"
    NOTLABELLED = "NOT LABELLED"

@dataclass
class GroundTruthEntry:
    query: str
    query_id: str
    relevance_scores: OrderedDict[str, Relevance] # doc_id : score)

@dataclass
class GroundTruth:
    entries: dict[str, GroundTruthEntry]

    def __getitem__(self, query_id: str) -> GroundTruthEntry:
        return self.entries[query_id]

    def __setitem__(self, query_id: str, entry: GroundTruthEntry) -> None:
        self.entries[query_id] = entry

    def __iter__(self) -> Iterator[str]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def values(self):
        return self.entries.values()

    def items(self):
        return self.entries.items()

    def keys(self):
        return self.entries.keys()
    

@dataclass
class PredictionsEntry:
    query: str
    query_id: str
    ranked_list: list[Document]
    
@dataclass
class Predictions:
    entries: dict[str, PredictionsEntry]

    def __getitem__(self, query_id: str) -> PredictionsEntry:
        return self.entries[query_id]

    def __setitem__(self, query_id: str, entry: PredictionsEntry) -> None:
        self.entries[query_id] = entry

    def __iter__(self) -> Iterator[str]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def values(self):
        return self.entries.values()

    def items(self):
        return self.entries.items()

    def keys(self):
        return self.entries.keys()