from insights.config import Profile
from insights.scoring import score_text


def test_score_text_basic():
    profile = Profile(
        name="test",
        start_urls=["https://example.com"],
        max_depth=1,
        same_domain_only=True,
        required_keywords=["devops"],
        bonus_keywords=["aws"],
        min_score=1,
        max_pages=10,
        request_delay_seconds=0.0,
        allowed_domains=None,
    )
    text = "This is a DevOps role using AWS in the cloud."
    result = score_text(text, profile)

    assert result.score > 0
    assert any(
        kw.lower() == "devops" for kw in (kw.lower() for kw in result.matched_required)
    )
    assert any(
        kw.lower() == "aws" for kw in (kw.lower() for kw in result.matched_bonus)
    )
