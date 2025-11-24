from typing import Optional


SYSTEM_PROMPT = """
You are an experienced SRE / DevOps engineer.

Given a chunk of log lines, you will:

1. Summarize the main issues and events.
2. Identify the top 3 likely root causes, if any.
3. Suggest concrete remediation steps.
4. Call out anything security-related or suspicious.
5. Suggest any observability / monitoring improvements.

Your response MUST be valid JSON with this shape:

{
  "summary": "...",
  "top_issues": [
    {"issue": "...", "evidence": "..."},
    ...
  ],
  "likely_root_causes": [
    {"cause": "...", "confidence": "low|medium|high"},
    ...
  ],
  "suggested_fixes": [
    "...",
    "..."
  ],
  "security_flags": [
    "...",
    "..."
  ],
  "observability_recommendations": [
    "...",
    "..."
  ]
}
""".strip()


def build_user_prompt(
    log_text: str,
    context: Optional[str] = None,
    source_name: Optional[str] = None,
) -> str:
    """
    Build the user prompt with optional context (e.g. 'nginx access logs')
    and source name (e.g. file name or pod name).
    """
    header_lines = []

    if source_name:
        header_lines.append(f"Source: {source_name}")
    if context:
        header_lines.append(f"Context: {context}")

    header = "\n".join(header_lines) if header_lines else "Log snippet:"

    return f"{header}\n\n```\n{log_text}\n```"
