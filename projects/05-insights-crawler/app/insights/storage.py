from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import csv


@dataclass
class PageResult:
    url: str
    title: str
    status_code: Optional[int]
    elapsed_ms: Optional[float]
    score: float
    matched_required: List[str]
    matched_bonus: List[str]
    snippet: str
    skipped_by_robots: bool
    error: Optional[str]


class ResultStore:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def save_csv(self, results: List[PageResult]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "url",
                    "title",
                    "status_code",
                    "elapsed_ms",
                    "score",
                    "matched_required",
                    "matched_bonus",
                    "snippet",
                    "skipped_by_robots",
                    "error",
                ]
            )
            for r in results:
                writer.writerow(
                    [
                        r.url,
                        r.title,
                        r.status_code,
                        r.elapsed_ms,
                        f"{r.score:.2f}",
                        ";".join(r.matched_required),
                        ";".join(r.matched_bonus),
                        r.snippet,
                        "true" if r.skipped_by_robots else "false",
                        r.error or "",
                    ]
                )
