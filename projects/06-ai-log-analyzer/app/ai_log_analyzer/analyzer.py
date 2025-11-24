import os

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from .config import OpenAIConfig
from .prompts import SYSTEM_PROMPT, build_user_prompt


@dataclass
class AnalysisResult:
    raw: Dict[str, Any]

    @property
    def summary(self) -> str:
        return self.raw.get("summary", "")

    @property
    def top_issues(self) -> Any:
        return self.raw.get("top_issues", [])

    @property
    def likely_root_causes(self) -> Any:
        return self.raw.get("likely_root_causes", [])

    @property
    def suggested_fixes(self) -> Any:
        return self.raw.get("suggested_fixes", [])

    @property
    def security_flags(self) -> Any:
        return self.raw.get("security_flags", [])

    @property
    def observability_recommendations(self) -> Any:
        return self.raw.get("observability_recommendations", [])


class LogAnalyzer:
    """
    High-level API for analyzing log text via direct HTTP call to OpenAI.

    This avoids the need for the 'openai' Python package and keeps dependencies minimal.
    """

    def __init__(self, config: Optional[OpenAIConfig] = None) -> None:
        self.config = config or OpenAIConfig.from_env()

    def analyze(
        self,
        log_text: str,
        *,
        context: Optional[str] = None,
        source_name: Optional[str] = None,
        temperature: float = 0.0,
    ) -> AnalysisResult:
        """
        Analyze the given log text and return a structured result.
        """
        if not log_text.strip():
            raise ValueError("log_text is empty")

        user_content = build_user_prompt(
            log_text=log_text,
            context=context,
            source_name=source_name,
        )

        # ---------------------------------------
        # DEMO MODE — bypass OpenAI API entirely
        # ---------------------------------------
        demo_mode = os.getenv("AI_LOG_ANALYZER_DEMO_MODE") == "1"
        if demo_mode:
            example = {
                "summary": (
                    "Demo mode: simulated analysis of logs showing DB "
                    "timeouts, microservice crashes, and authentication failures."
                ),
                "top_issues": [
                    {
                        "issue": "Database connection timeouts",
                        "evidence": "ERROR timeout connecting to PostgreSQL on port 5432",
                    },
                    {
                        "issue": "Authentication 503 errors",
                        "evidence": "Authentication service responded with 503",
                    },
                ],
                "likely_root_causes": [
                    {
                        "cause": "Database under load or slow queries",
                        "confidence": "medium",
                    },
                    {
                        "cause": "Auth microservice crash loop",
                        "confidence": "medium",
                    },
                ],
                "suggested_fixes": [
                    "Check PostgreSQL slow query logs.",
                    "Restart auth service + inspect stack traces.",
                    "Add alerts for DB latency and 5xx error spikes.",
                ],
                "security_flags": [
                    "Ensure detailed stack traces are not returned to clients."
                ],
                "observability_recommendations": [
                    "Add a dashboard for DB connection latency.",
                    "Add alerts for auth 5xx spikes.",
                ],
            }
            return AnalysisResult(raw=example)

        payload = {
            "model": self.config.model,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        }

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )

        if response.status_code == 429:
            # Rate limit / quota exceeded
            raise RuntimeError(
                "OpenAI API returned 429 Too Many Requests. "
                "This usually means your free credits are exhausted or you need to add billing."
            )

        response.raise_for_status()

        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "{}")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Model returned invalid JSON: {exc}") from exc

        return AnalysisResult(raw=parsed)
