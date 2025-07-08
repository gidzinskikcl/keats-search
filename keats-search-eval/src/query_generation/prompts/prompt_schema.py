from dataclasses import dataclass
import enum


class Role(enum.Enum):
    SYSTEM = "system"
    USER = "user"


@dataclass
class Prompt:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role.value, "content": self.content}


@dataclass
class PromptHistory:
    system_prompt: Prompt
    user_prompt: Prompt
