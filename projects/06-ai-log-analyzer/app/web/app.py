from __future__ import annotations

import io

# from pathlib import Path
from typing import Optional

from flask import (
    Flask,
    render_template,
    request,
    send_file,
)

from ai_log_analyzer.analyzer import LogAnalyzer, AnalysisResult

app = Flask(__name__)
analyzer = LogAnalyzer()


@app.route("/", methods=["GET", "POST"])
def index():
    analysis: Optional[AnalysisResult] = None
    error: Optional[str] = None
    log_preview: Optional[str] = None

    if request.method == "POST":
        context = request.form.get("context") or None
        log_text = request.form.get("log_text") or ""
        file = request.files.get("log_file")

        if file and file.filename:
            log_text = file.read().decode("utf-8", errors="ignore")

        if not log_text.strip():
            error = "Please paste logs or upload a log file."
            return render_template(
                "index.html",
                error=error,
                analysis=None,
                log_preview=None,
            )

        log_preview = "\n".join(log_text.splitlines()[:50])

        try:
            analysis = analyzer.analyze(
                log_text=log_text,
                context=context,
                source_name=file.filename if file else "pasted logs",
            )
        except Exception as exc:  # noqa: BLE001
            error = f"Error during analysis: {exc}"
            analysis = None

    return render_template(
        "index.html",
        error=error,
        analysis=analysis,
        log_preview=log_preview,
    )


@app.route("/download-json", methods=["POST"])
def download_json():
    """
    Download the last analysis JSON directly from the browser.

    In a real app, you'd store per-session state. For this portfolio
    demo, we just re-run the analysis on demand for download.
    """
    context = request.form.get("context") or None
    log_text = request.form.get("log_text") or ""
    file = request.files.get("log_file")

    if file and file.filename:
        log_text = file.read().decode("utf-8", errors="ignore")

    if not log_text.strip():
        return "No log data to analyze.", 400

    analysis = analyzer.analyze(
        log_text=log_text,
        context=context,
        source_name=file.filename if file else "pasted logs",
    )

    import json

    data = json.dumps(analysis.raw, indent=2)
    buf = io.BytesIO(data.encode("utf-8"))
    return send_file(
        buf,
        mimetype="application/json",
        as_attachment=True,
        download_name="log-analysis.json",
    )
