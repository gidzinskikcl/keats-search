from abc import ABC, abstractmethod

class PromptBuilder(ABC):
    
    @staticmethod
    @abstractmethod
    def build(course_name: str, num_questions: int, lecture_content: str) -> list[dict[str, str]]:
        pass