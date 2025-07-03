from abc import ABC

class TranscriptGateway(ABC):
    def get(self, url: str) -> dict:
        pass