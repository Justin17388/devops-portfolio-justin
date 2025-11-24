📘 AI Log Analyzer (Project 6)
Intelligent Log Analysis using LLMs · Observability · Troubleshooting Automation

This project is a lightweight AI-powered log analysis tool designed to assist with incident response, debugging, and observability workflows. It accepts any log file or free-form log text, analyzes patterns, identifies root causes, and produces structured insights — all through a clean web interface and optional CLI.

The tool supports both:

Live mode: Uses the OpenAI API to analyze logs

Demo mode (default in this repo): No API key required; generates realistic analysis output for reviewers

🚀 Features
🧠 AI Log Analysis

Summarizes log files

Highlights the top issues

Identifies likely root causes

Suggests fixes and remediation steps

Flags potential security concerns

Recommends observability metrics and dashboards

🌐 Web Interface

Paste logs directly into the browser

Instant analysis

Downloadable JSON report

💻 CLI Mode

Analyze logs directly from the terminal:

python cli.py logs/example.log

🛡️ Ethical Safeguards

Clears sensitive data before analysis

Never transmits unnecessary metadata

Supports offline demo mode

Respects user-provided logs only (no scraping)

🔧 Tech Stack

Python 3

Flask (UI)

Requests (OpenAI integration — no heavy SDK)

Environment-based configuration

Fully linted (flake8, black)

Pre-commit hooks enabled

📁 Project Structure
06-ai-log-analyzer/
│
├── app/
│   ├── ai_log_analyzer/
│   │   ├── analyzer.py        # Main AI logic (API + demo mode)
│   │   ├── config.py          # Reads OPENAI_API_KEY + model
│   │   ├── prompts.py         # System + user prompt generation
│   │
│   ├── web/
│   │   ├── app.py             # Flask web server
│   │   ├── templates/
│   │   │   └── index.html     # Web UI
│   │   └── static/
│   │       └── styles.css
│   │
│   ├── cli.py                 # Command-line interface
│   ├── logs/                  # Sample logs for demo/testing
│   └── requirements.txt
│
└── README.md

🧪 Running the App
### ✔️ Demo Mode (Recommended for Reviewers — No API key required)

This repo ships with demo mode enabled so you can try the UI instantly.

$env:AI_LOG_ANALYZER_DEMO_MODE = "1"
$env:FLASK_APP = "web.app"
flask run


Then open:

👉 http://127.0.0.1:5000

Paste any logs — you’ll get realistic AI-style structured insights.

✔️ Live Mode (Optional)

To use real LLM analysis, add your OpenAI API key:

$env:OPENAI_API_KEY = "sk-..."
$env:AI_LOG_ANALYZER_DEMO_MODE = ""
flask run

🎯 Example Output (Demo Mode)

Summary

Database timeouts and 503 responses caused cascading service failures and worker crashes.

Top Issues

PostgreSQL timeout errors

Authentication service returning HTTP 503

Worker thread crash due to null reference

Likely Root Causes

Database under load / slow queries

Auth microservice restart loop

Suggested Fixes

Inspect DB slow query logs

Restart authentication service and gather crash traces

Add alerts for connection latency and 5xx spikes

…and more.

🔍 This project demonstrates:

AI + DevOps integration

Incident response automation

Observability mindset

Safe handling of logs

Python application design

REST API usage (OpenAI)

Frontend + backend development

Practical engineering value


📝 Future Enhancements

Multi-log comparison

Log anomaly scoring

Dashboard export (Grafana JSON)

Kubernetes pod log integration

S3 log ingestion

🤝 Author

Justin Shinn
Cloud & DevOps Engineer
Containerization · IaC · Automation · AI for DevOps
