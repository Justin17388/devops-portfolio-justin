import os
from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Please export it in your environment."
            )
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return cls(api_key=api_key, model=model)
