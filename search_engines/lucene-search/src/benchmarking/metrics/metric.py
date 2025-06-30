from abc import ABC, abstractmethod

from benchmarking.schemas import schemas

class Metric(ABC):

    @abstractmethod
    def evaluate(self, ground_truth_entry: schemas.GroundTruthEntry, ranked_list: list[schemas.Document]) -> float:
        pass