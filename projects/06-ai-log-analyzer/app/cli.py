import argparse
from pathlib import Path

from ai_log_analyzer.analyzer import LogAnalyzer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-powered log analyzer (DevOps/SRE focused)."
    )
    parser.add_argument(
        "log_file",
        type=str,
        help="Path to the log file to analyze",
    )
    parser.add_argument(
        "--context",
        type=str,
        default="",
        help="Optional context (e.g. 'nginx access logs')",
    )
    args = parser.parse_args()

    log_path = Path(args.log_file)
    if not log_path.is_file():
        raise SystemExit(f"Log file not found: {log_path}")

    log_text = log_path.read_text(encoding="utf-8", errors="ignore")

    analyzer = LogAnalyzer()
    result = analyzer.analyze(
        log_text=log_text,
        context=args.context or None,
        source_name=str(log_path),
    )

    print("\n=== Summary ===")
    print(result.summary)

    print("\n=== Top Issues ===")
    for issue in result.top_issues:
        print(f"- {issue.get('issue')} (evidence: {issue.get('evidence')})")

    print("\n=== Likely Root Causes ===")
    for cause in result.likely_root_causes:
        print(f"- {cause.get('cause')} " f"(confidence: {cause.get('confidence')})")

    print("\n=== Suggested Fixes ===")
    for fix in result.suggested_fixes:
        print(f"- {fix}")

    print("\n=== Security Flags ===")
    for flag in result.security_flags:
        print(f"- {flag}")

    print("\n=== Observability Recommendations ===")
    for rec in result.observability_recommendations:
        print(f"- {rec}")


if __name__ == "__main__":
    main()
