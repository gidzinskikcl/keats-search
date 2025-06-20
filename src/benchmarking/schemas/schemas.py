from dataclasses import dataclass

from typing import Iterator, OrderedDict

import enum

@dataclass
class Document:
    doc_id: str
    content: str

@dataclass
class Query:
    id: str
    question: str

class RelevanceScore(enum.Enum):
    IRRELEVANT = 0
    SLIGHTLY_RELEVANT = 1
    MODERATELY_RELEVANT = 2
    HIGHLY_RELEVANT = 3

@dataclass
class GroundTruthEntry:
    query: str
    query_id: str
    relevance_scores: OrderedDict[str, RelevanceScore] # doc_id : score)

    def get_score(self, doc_id: str) -> RelevanceScore:
        """Returns the relevance score for a given segment ID. Defaults to IRRELEVANT if not found."""
        return self.relevance_scores.get(doc_id, RelevanceScore.IRRELEVANT)

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