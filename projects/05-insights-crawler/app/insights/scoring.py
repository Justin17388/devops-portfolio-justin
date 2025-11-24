from dataclasses import dataclass
from typing import List

from .config import Profile


@dataclass
class ScoreResult:
    score: float
    matched_required: List[str]
    matched_bonus: List[str]


def score_text(text: str, profile: Profile) -> ScoreResult:
    """
    Basic NLP-style scoring:
    - +2 for each required keyword found
    - +1 for each bonus keyword found
    - plus a small boost based on keyword density in the text
    """
    text_lower = text.lower()
    matched_required: List[str] = []
    matched_bonus: List[str] = []
    score = 0.0

    for kw in profile.required_keywords:
        if kw.lower() in text_lower:
            matched_required.append(kw)
            score += 2.0

    for kw in profile.bonus_keywords:
        if kw.lower() in text_lower:
            matched_bonus.append(kw)
            score += 1.0

    # Simple density boost: more keywords in shorter text => slightly higher score
    words = text_lower.split()
    if words and (matched_required or matched_bonus):
        keyword_tokens = [
            token
            for kw in profile.required_keywords + profile.bonus_keywords
            for token in kw.lower().split()
        ]
        keyword_hits = sum(text_lower.count(tok) for tok in set(keyword_tokens))
        density = keyword_hits / max(20, len(words))  # avoid division by tiny docs
        score += density * 5.0  # small boost

    return ScoreResult(
        score=score,
        matched_required=matched_required,
        matched_bonus=matched_bonus,
    )
