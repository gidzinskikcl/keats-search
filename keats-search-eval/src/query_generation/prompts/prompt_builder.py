from abc import ABC, abstractmethod

from query_generation.prompts import templates

class PromptBuilder(ABC):
    
    @staticmethod
    @abstractmethod
    def build(course_name: str, num_questions: int, lecture_content: str, prompt_module: templates.PromptTemplate) -> list[dict[str, str]]:
        pass