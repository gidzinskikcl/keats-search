from abc import ABC
from dataclasses import dataclass, asdict

@dataclass
class Document(ABC):
    """
    Abstract base class for documents, defining common attributes and methods.
    This class is not meant to be instantiated directly.
    """
    doc_id: str

def to_dict(docs: list[Document]) -> list[dict[str, str]]:
    result = [asdict(doc) for doc in docs]
    return result